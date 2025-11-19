import pdfplumber
import os
import re

# 1. 경로 설정
PATH = os.path.dirname(os.path.dirname(__file__))
BASE_PDF_DIR = os.path.join(PATH, "pdfFiles")
BASE_DB_DIR = os.path.join(PATH, "curriculum_db")
target_dirs = ["computer_science", "humanitas"]

# 2. 텍스트 정제 함수 (레이아웃 모드용)
def clean_text_layout(text):
    if not text: return ""
    
    # (1) 이상한 특수문자 제거 (필요하면 추가)
    text = re.sub(r'[◩■●•]', '', text)
    
    # (2) 불필요한 헤더/푸터 패턴 제거 (예: "305 2022학년도...")
    # 페이지마다 반복되는 번호나 제목을 지웁니다.
    text = re.sub(r'\n\s*\d{2,3}\s+20\d{2}학년도 교육과정', '', text)
    
    # (3) 연속된 빈 줄(3줄 이상)은 하나로 줄이기 (너무 휑하지 않게)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

print("🚀 '눈에 보이는 그대로' 변환 시작 (Layout 모드)...")

for target in target_dirs:
    input_dir = os.path.join(BASE_PDF_DIR, target)
    output_dir = os.path.join(BASE_DB_DIR, target)
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(input_dir): continue
    
    files = os.listdir(input_dir)
    print(f"\n📂 [{target}] 처리 중...")

    for file in files:
        if file.startswith(".") or not file.endswith(".pdf"): continue
        
        pdf_path = os.path.join(input_dir, file)
        txt_filename = os.path.splitext(file)[0] + ".txt"
        output_path = os.path.join(output_dir, txt_filename)
        
        print(f"  - 변환 중: {file}")

        try:
            full_content = ""
            
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    # [핵심 기술] layout=True
                    # 텍스트의 물리적 위치를 공백(Space)으로 표현하여 레이아웃을 보존합니다.
                    # x_tolerance: 글자 간격 허용치 (기본값보다 조금 줄여서 단어 뭉침 방지)
                    try:
                        # 헤더/푸터 영역 잘라내기 (위 50, 아래 60 제외)
                        cropped_page = page.crop((0, 50, page.width, page.height - 60))
                        text = cropped_page.extract_text(layout=True, x_tolerance=2, y_tolerance=3)
                    except ValueError:
                        # crop 실패 시 원본 사용
                        text = page.extract_text(layout=True, x_tolerance=2, y_tolerance=3)

                    if text:
                        cleaned_text = clean_text_layout(text)
                        full_content += cleaned_text + "\n\n"
                        full_content += "-" * 50 + "\n\n" # 페이지 구분선

            # 결과 저장
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_content)
                
        except Exception as e:
            print(f"  ❌ 에러 발생 ({file}): {e}")

print("\n✨ 변환 완료! 텍스트 파일을 열어서 표 모양이 유지되었는지 확인해보세요.")