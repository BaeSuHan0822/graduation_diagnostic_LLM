import os
from Kanana import Custom_Kanana
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

model = Custom_Kanana()

file_path = "../curriculum_db/"
output_path = "../chroma_db"
if os.path.exists(output_path) :
    print("이미 존재합니다.")
else :
    os.makedirs(output_path)
files = os.listdir(file_path)

for file in files :
    loader = TextLoader(file_path + file)
    loader = loader.load()
    
    pages = [page.page_content for page in loader]
    text = "\n".join(pages)
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 0,
        separators = [".","?","!","\n"]
    )
    
    sentences = splitter.split_text(text)
    
    vector_store = Chroma(
        collection_name = file.split(".")[0] + "txt",
        embedding_function = model,
        persist_directory = output_path,
    )
    
    