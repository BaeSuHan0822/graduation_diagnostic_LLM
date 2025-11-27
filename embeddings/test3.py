import os
from dotenv import load_dotenv
from llama_parse import LlamaParse

# 환경 변수 로드
load_dotenv()

# 경로 설정
PATH = os.path.dirname(os.path.dirname(__file__))
PDF_BASE_PATH = os.path.join(PATH, "pdfFiles")
DB_BASE_PATH = os.path.join(PATH, "curriculum_db")
sub_folder = ["computer_science", "humanitas"]

# ✅ LlamaParse 설정 최적화 (핵심)
# 1. result_type="markdown": 텍스트와 표를 알아서 가장 깔끔한 MD 포맷으로 변환해줍니다.
# 2. parsing_instruction: LLM에게 표 처리에 집중하라고 명시합니다.
instruction = """
This is a university curriculum document containing graduation requirements and course descriptions.
Please preserve the structure of tables accurately in Markdown format.
Do not skip complex tables outlining credits and course categories.
"""

parser = LlamaParse(
    result_type="markdown",  # JSON 대신 Markdown 사용
    language="ko",
    verbose=True,
    parsing_instruction=instruction
)

print("🚀 파싱 시작...")

for folder in sub_folder:
    input_dir = os.path.join(PDF_BASE_PATH, folder)
    output_dir = os.path.join(DB_BASE_PATH, folder)
    
    # 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 입력 폴더가 존재하는지 확인
    if not os.path.exists(input_dir):
        print(f"⚠️ 경고: 입력 폴더가 없습니다 -> {input_dir}")
        continue

    files = os.listdir(input_dir)
    
    for file in files:
        if file.startswith("."):
            continue
        
        pdf_file_path = os.path.join(input_dir, file)
        file_name = os.path.splitext(file)[0]
        md_file_path = os.path.join(output_dir, file_name + ".md")
        
        print(f"🔄 처리 중: {file} ...")
        
        try:
            # LlamaParse로 로드 (이미 Markdown으로 변환됨)
            documents = parser.load_data(pdf_file_path)
            
            # 여러 페이지로 나뉜 결과를 하나의 텍스트로 병합
            # page_content 대신 text 속성을 사용해야 함 (LlamaIndex Document 객체 기준)
            full_markdown = "\n\n".join([doc.text for doc in documents])
            
            # 파일 저장
            with open(md_file_path, "w", encoding="utf-8") as f:
                f.write(full_markdown)
            
            print(f"    ✅ 저장 완료: {md_file_path}")
            
        except Exception as e:
            print(f"    ❌ 에러 발생 ({file}): {e}")

print("✨ 모든 작업이 완료되었습니다.")