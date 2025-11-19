import pdfplumber
import os
import re

PATH = os.path.dirname(os.path.dirname(__file__))
computer_file_path = os.path.join(PATH,"pdfFiles","computer_science")
humanitas_file_path = os.path.join(PATH,"pdfFiles","humanitas")
computer_files = os.listdir(computer_file_path)
humanitas_files = os.listdir(humanitas_file_path)
computer_output_path = os.path.join(PATH,"curriculum_db","computer_science")
humanitas_output_path = os.path.join(PATH,"curriculum_db","humanitas")

def clean_text(text):
    if not text:
        return ""
    
    # (1) 불필요한 특수문자 제거 (◩, ■, 이상한 공백 등)
    text = re.sub(r'[◩■●•]', '', text) 
    
    # (2) 페이지 번호나 헤더 텍스트 패턴 제거 (예: "301 2022학년도...")
    # (이 부분은 crop으로 대부분 해결되지만 혹시 몰라 추가)
    text = re.sub(r'\d{2,3}\s+20\d{2}학년도 교육과정', '', text)

    # (3) 문장 중간의 줄바꿈 없애기 (한글 뒤에 오는 줄바꿈만 공백으로 변경)
    # "정보를\n수집하고" -> "정보를 수집하고"
    text = text.replace("\n", " ") 
    
    # (4) 다중 공백을 하나로 줄이기
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

for file in computer_files :
    if file.startswith(".") :
        continue
    name = str(file.split(".")[0]) + ".txt"
    output_path = os.path.join(computer_output_path,name)
    print(os.path.join(computer_file_path,file))
    
    with pdfplumber.open(os.path.join(computer_file_path,file)) as F :
        full_text = ""
        
        for i,page in enumerate(F.pages) :
            text = page.extract_text()
            full_text += text + "\n"
            
    with open(output_path,"w",encoding = "utf-8") as f :
        f.write(full_text)
        
for file in humanitas_files :
    if file.startswith(".") :
        continue
    name = str(file.split(".")[0]) + ".txt"
    output_path = os.path.join(humanitas_output_path,name)
    print(os.path.join(humanitas_file_path,file))
    
    with pdfplumber.open(os.path.join(humanitas_file_path,file)) as F :
        full_text = ""
        
        for i,page in enumerate(F.pages) :
            text = page.extract_text()
            full_text += text + "\n"
            
    with open(output_path,"w",encoding = "utf-8") as f :
        f.write(full_text)