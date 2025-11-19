import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from langchain_classic.schema import Document

load_dotenv()

PATH = os.path.dirname(os.path.dirname(__file__))
PDF_BASE_PATH = os.path.join(PATH,"pdfFiles")
DB_BASE_PATH = os.path.join(PATH,"curriculum_db")
sub_folder = ["computer_science","humanitas"]

parser = LlamaParse(
    result_type="markdown",
    language="ko"
)

for folder in sub_folder :
    input_dir = os.path.join(PDF_BASE_PATH,folder)
    output_dir = os.path.join(DB_BASE_PATH,folder)
    os.makedirs(output_dir,exist_ok = True)
    
    files = os.listdir(input_dir)
    
    for file in files :
        if file.startswith(".") :
            continue
        
        pdf_file_path = os.path.join(input_dir,file)
        file_name = os.path.splitext(file)[0]
        md_file_path = os.path.join(output_dir,file_name+".md")
        
        try :
            documents = parser.load_data(pdf_file_path)
            
            md_text = ""
            for doc in documents :
                md_text += doc.text + "\n\n"
                
            with open(md_file_path,"w",encoding = "utf-8") as f :
                f.write(md_text)
            
            print(f"    ✅ 저장 완료: {md_file_path}")
        except Exception as e :
            print(f"    ❌ 에러 발생: {e}")