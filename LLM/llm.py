import os
import re
from typing import Dict, List, Optional
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tabulate import tabulate

# --- 1. 설정 및 DB 로드 ---
SHARED_PATH = "/LLM/chroma-db"
persist_directory = SHARED_PATH

embedding_function = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-small",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

computer_db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_function,
    collection_name="computer_science",
)


# --- 2. 입력 텍스트 처리 ---
SECTION_PATTERN = re.compile(r"\[(.+?)\]\n(.*?)(?=\n\[|$)", re.S)

def build_student_payload(raw_text: str) -> str:
    return raw_text


def split_sections(raw_text: str) -> Dict[str, str]:
    sections = {}
    for match in SECTION_PATTERN.finditer(raw_text):
        section_name = match.group(1).strip()
        section_body = match.group(2).strip()
        sections[section_name] = section_body
    return sections


def _parse_credit(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    matches = re.findall(r"\d+", value)
    return int(matches[0]) if matches else None


def _sanitize_major(raw_major: Optional[str]) -> str:
    major = (raw_major or "컴퓨터공학과").strip()
    return major.replace("학부", "학과") if "학부" in major else major


def extract_student_info(sections: Dict[str, str]) -> Dict:
    info_section = sections.get("개인 정보", "")
    criteria_section = sections.get("졸업 기준", "")
    status_section = sections.get("학생 이수 현황", "")

    def _line_value(section_text: str, label: str) -> Optional[str]:
        pattern = re.compile(rf"-\s*{re.escape(label)}\s*:\s*(.+)")
        for line in section_text.splitlines():
            match = pattern.match(line.strip())
            if match:
                return match.group(1).strip()
        return None

    student_id = _line_value(info_section, "학번") or "미상"
    name = _line_value(info_section, "성명") or "미상"
    major = _sanitize_major(_line_value(info_section, "학과") or "컴퓨터공학과")
    curriculum_year = _line_value(info_section, "졸업기준학점(년도)") or "2022"
    required_credits = _parse_credit(_line_value(criteria_section, "취득학점"))
    earned_credits = _parse_credit(_line_value(status_section, "취득학점"))

    return {
        "student_id": student_id,
        "name": name,
        "major": major,
        "curriculum_year": curriculum_year,
        "required_credits": required_credits,
        "earned_credits": earned_credits,
    }


def _format_table(rows: List[List], headers: List[str]) -> str:
    if not rows:
        return ""
    if tabulate:
        return tabulate(rows, headers=headers, tablefmt="github")

    widths = [len(str(header)) for header in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(str(cell)))

    def _fmt_row(row_values):
        return " | ".join(str(value).ljust(widths[idx]) for idx, value in enumerate(row_values))

    lines = [
        _fmt_row(headers),
        "-+-".join("-" * width for width in widths),
    ]
    for row in rows:
        lines.append(_fmt_row(row))
    return "\n".join(lines)


def retrieve_rule_documents(year: str, major: str):
    queries = [
        f"query: {year}학년도 {major} 전공필수 과목 리스트 표",
        f"query: {year}학년도 {major} 졸업 이수 학점 기준",
    ]

    retrieved_docs = []
    for query in queries:
        retrieved_docs.extend(computer_db.similarity_search(query, k=1))

    unique_docs = []
    seen = set()
    for doc in retrieved_docs:
        content_key = doc.page_content
        if content_key in seen:
            continue
        seen.add(content_key)
        unique_docs.append(doc)

    return unique_docs


def build_context_text(documents) -> str:
    context_text = ""
    for idx, doc in enumerate(documents, start=1):
        clean_content = doc.page_content.replace("passage: ", "")
        source = doc.metadata.get("source", "")
        context_text += f"\n[학칙 문서 {idx}] (출처: {source})\n{clean_content}\n"
    return context_text

# --- 3. 메인 진단 함수 ---
def diagnose_graduation(raw_text : str):
    if not raw_text:
        return

    sections = split_sections(raw_text)
    prompt_payload = build_student_payload(raw_text)
    student_info = extract_student_info(sections)

    documents = retrieve_rule_documents(student_info["curriculum_year"], student_info["major"])
    context_text = build_context_text(documents)

    llm = ChatOllama(
        model="tinyllama:1.1b", 
        temperature=0.1,
        base_url="http://localhost:11434",
        num_ctx=2048
    )
    
    template = """
    당신은 대학교 졸업 사정관입니다. 
    제공된 [학칙]과 [학생 성적표]를 대조하여 졸업 가능 여부를 분석하고 보고서를 작성하세요.
    
    ---
    [학칙 문서 (졸업 요건)]:
    {context_text}
    
    [학생 성적표]:
    {raw_text}
    ---

    **반드시 아래 순서대로 생각하고 답변을 작성하세요:**

    1. **기준 확인**: 학칙에서 이 학생(입학년도, 학과)이 들어야 하는 '전공필수 과목 리스트'와 '졸업 기준 학점'을 찾아서 명시하세요.
    2. **수강 대조**: 학생이 수강한 과목 목록과 학칙의 전공필수 과목을 하나씩 비교하세요. 
       - (주의: 과목명 앞의 'se', 'e' 같은 접두사는 무시하고 비교할 것)
    3. **학점 계산**: [취득 학점]이 [기준 학점]보다 부족한지 확인하세요.
    4. **결론 도출**: 
       - 졸업 '가능' 또는 '불가능'을 명확히 밝히세요.
       - 불가능하다면, "어떤 과목이 누락되었는지", "몇 학점이 부족한지" 구체적으로 나열하세요.

    **[졸업 사정 결과 보고서]**
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {
            "raw_text": lambda _: prompt_payload,
            "context_text": lambda _: context_text,
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    try:
        response = chain.invoke({})
        return response
    except Exception as e:
        print(f"❌ LLM 생성 중 오류 발생: {e}")