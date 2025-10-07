import os
import re
import json
from typing import List, Dict, Any

def parse_personal_info_report(file_path : str) -> Dict[str,Any] :
    """
    졸업진단표에서 필요한 부분을 따로 추출하는 함수입니다. 졸업진단표는 txt 파일로 저장한 후 파싱하여 구조화된 딕셔너리로 변환합니다.
    """
    with open(file_path, 'r', encoding = "cp949") as f :
        full_text = f.read()
        lines = full_text.splitlines()
        
    report_data = {} # 최종결과를 저장할 딕셔너리
    
    # 1. 개인정보 추출하기
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

#     # 3. 교양,전공 등 수강과목 리스트 추출
#     current_section = None
#     all_courses = {} # 정보를 저장할 딕셔너리
    
#     for line in lines :
#         section_match = re.search(r"\[\s*(.+?)\s*\]",line)
#         if section_match :
#             current_section = section_match.group(1)
#             if current_section not in all_courses :
#                 all_courses[current_section] = []
#             continue
        
#         if current_section :
#             course_pattern = re.compile(
#                 r"([A-Z]{2,}\d{3,})\s+"      # 그룹 1: 학수번호
#                 r"(.+?)\s+"            # 그룹 2: 과목명 (공백 포함)
#                 r"(\d+(?:\.\d)?)\s+"   # 그룹 3: 학점 (예: 3 또는 3.0)
#                 r"([A-F][0\+]?)\s+"    # 그룹 4: 등급
#                 r"(\d{4}\s*/\s*\d+.*)" # 그룹 5: 수강학기
#             )
            
#             course_match = course_pattern.search(line)
#             if course_match :
#                 code, name, credit, grade, semester = course_match.groups()
#                 all_courses[current_section].append({
#                     "학수번호" : code.strip(),
#                     "과목명" : name.strip(),
#                     "학점" : float(credit),
#                     "등급" : grade.strip(),
#                     "수강학기" : semester.strip()
#                 })
                
#     report_data.update(all_courses)
#     return report_data


# if __name__ == "__main__" :
#     INPUT_FILE_PATH = "data/noname.txt"
#     OUTPUT_DIR = "output"
#     OUTPUT_FILE_NAME = "parsed_report.json"
    
#     os.makedirs(OUTPUT_DIR, exist_ok = True)
#     output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE_NAME)
    
#     try : 
#         parsed_report = parse_graduation_report(INPUT_FILE_PATH)
#         print("파일 파싱 성공 !")
        
#         with open(output_path, 'w', encoding = "utf-8") as f :
#             json.dump(parsed_report, f, indent = 2, ensure_ascii = False)
        
#         print("\n--------------최종 파싱 결과---------------")
#         with open(output_path, 'r', encoding = "utf-8") as f :
#             print(f.read())
#         print("\n----------------------------------------")
    
#     except FileNotFoundError :
#         print(f"파일을 찾을 수 없습니다 : {INPUT_FILE_PATH}")
#     except Exception as e :
#         print(f"파일을 읽거나 처리하는 중 에러가 났습니다 ! : {INPUT_FILE_PATH, e}")

def parse_subject_report(file_path : str) -> Dict[str,Any] :
    with open(file_path, "r", encoding = "cp949") as f :
        full_text = f.read()
        lines = full_text.splitlines()
        
        pattern = re.compile(r"교양/기타/금학기수강학점\s+전공학점")
        
        for line_numbers, line_content in enumerate(lines,1) : # 수강한 과목들이 나와있는 헤더가 몇 번째 줄인지 찾기
            match = pattern.search(line_content)
            
            if match :
                print(f"헤더를 {line_numbers}에서 찾았습니다")
                print(f"찾은 내용 : {line_content.strip()}")
                break
            
        report_data = {} # 정보 저장
        patterns = re.compile(
            r"^\s*(\S+)\s+"               # 그룹 1: 구분 (줄 시작 부분의 첫 단어/숫자)
            r"([A-Z]{2,}\d{3,})\s+"      # 그룹 2: 학수번호 (영문+숫자)
            r"(.+?)\s+"                  # 그룹 3: 과목명 (공백 포함 가능)
            r"(\d+)\s+"                  # 그룹 4: 학점 (정수)
            r"(\d{4}\s*/\s*\d.*)"        # 그룹 5: 수강학기 (YYYY / N 형식)          
        )
        
        

parse_subject_report("data/noname.txt")