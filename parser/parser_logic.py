import re
import json
from typing import List, Dict, Any, Union

def parse_personal_info_report(full_text : str) -> Dict :
    lines = full_text.splitlines()
        
    report_data = {}
    
    personal_info = {}
    patterns = {
        "학번": r"학번\s*:?\s*(\d+)",
        "성명": r"성명\s*:?\s*([가-힣]+)",
        "학과": r"학과\s*:?\s*([가-힣]+)",
        "졸업기준학점(년도)": r"졸업기준학점\(년도\)\s*:?\s*([\d\.]+)",
        "외국인여부": r"외국인여부\s*:?\s*([A-Z])"
    }
    
    for key, pattern in patterns.items() :
        match = re.search(pattern,full_text)
        if match :
            personal_info[key] = match.group(1).strip()
            
    report_data["개인정보"] = personal_info
    return report_data


def parse_graduation(full_text : str) -> Dict :
    lines = full_text.splitlines()
        
    grad_block_match = re.search(
        r"졸업\s*판정(?P<block>[\s\S]*?)(?=\n\s*(?:전공|교양|전공내역|교양내역|금학기|졸업요건|모의기|$))",
        full_text,
        flags=re.M
    )
    
    grad_block = grad_block_match.group("block") if grad_block_match else full_text
    
    row_re = re.compile(
        r"""
        ^(?P<row>기준|취득|판정)\s+                 
        (?P<수강학점>\d+)\s+
        (?P<취득학점>\d+(?:\(\d+\))?)\s+           
        (?P<전공>\d+)\s+
        (?P<교양>\d+)\s+
        (?P<졸업평점>\d+(?:\.\d+)?)\s+
        (?P<영어강의>\d+)\s+
        (?P<논문>\d+)\s+
        (?P<TOPIK>해당없음|\S*)\s+
        (?P<졸능_구분>외국어|전산\(기타\)|최종판정)\s+
        (?P<졸능_판정>면제|통과|미통과)\s+
        (?P<SW_구분>단대\+후마|학점|\S+)\s+
        (?P<SW_판정>통과|미통과|\d+)
        \s*$
        """,
        flags=re.M | re.X
    )
    
    report_data = {}
    for m in row_re.finditer(grad_block) :
        gd = m.groupdict()
        row_label = gd.pop("row")
        report_data[row_label] = gd
        
    return report_data
    
    
def parse_class_info(full_text : str) -> Dict :
    lines = full_text.splitlines()

    course_block_match = re.search(
        r"교양\s*/?\s*기타\s*/?\s*금학기\s*수강학점\s*\t*\s*전공학점[\t ]*\n(?P<block>[\s\S]*?)(?=\n\s*(?:졸업\s*필수|졸업필수|연락처|상담자|$))",
        full_text,
        flags=re.M
    )
    
    course_block = course_block_match.group("block")
    
    COURSE_RE = re.compile(
        r"""
        ^\s*(?:\d{0,2}(?:\s*\d{1,2})?)?\s*         # 구분번호는 매칭만 하고 저장 X
        (?P<학수번호>[A-Z]{2,}\d{3,})\s+
        (?P<전공명>[가-힣A-Za-z0-9\.\+\(\)#\s:/-]+?)\s+
        (?P<학점>\d+)\s+
        (?P<수강학기>\d{4}\s*/\s*[12])(?:\s*계절)?
        """,
        flags=re.M | re.X
    )
    
    results = []
    current_category = None
    
    for line in course_block.splitlines() :
        if re.search(r"(필수교과|배분이수|자유이수|기타)",line) :
            current_category = line.strip().split()[0]
            continue
        
        m = COURSE_RE.search(line)
        if m :
            row = m.groupdict()
            row["전공명"] = row["전공명"].replace("#", "").strip()

            results.append(row)
            
    return {"수강과목" : results}
        
        
def merge_data_to_output(base_data : dict, key_name : str, item : dict | list) -> Dict :
    base_data[key_name] = item
    return base_data

def text_to_parsed_json(full_text : str) -> Dict :
    result = {}
    result = merge_data_to_output(result, "개인정보", parse_personal_info_report(full_text))
    result = merge_data_to_output(result, "졸업판정" ,parse_graduation(full_text))
    result = merge_data_to_output(result, "수강과목", parse_class_info(full_text))
    return result
