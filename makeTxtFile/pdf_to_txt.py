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

def table_to_markdown(table_data):
    if not table_data: return ""
    # None 값을 빈 문자열로 변환
    rows = [[str(cell) if cell else "" for cell in row] for row in table_data]
    if not rows: return ""

    markdown = ""
    # (1) 헤더 작성
    markdown += "| " + " | ".join(rows[0]) + " |\n"
    # (2) 구분선 작성 (|---|---|...)
    markdown += "| " + " | ".join(["---"] * len(rows[0])) + " |\n"
    # (3) 내용 작성
    for row in rows[1:]:
        markdown += "| " + " | ".join(row) + " |\n"
    
    return markdown + "\n"

for file in computer_files :
    if file.startswith(".") :
        continue
    name = os.path.splitext(file)[0] + ".txt"
    output_path = os.path.join(computer_output_path,name)
    print(os.path.join(computer_file_path,file))
    
    with pdfplumber.open(os.path.join(computer_file_path,file)) as PDF :
        full_text = ""
        
        for page in PDF.pages :
            tables = page.extract_table()
            
            for table in tables :
                print(table)
            
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