import os,shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_function = HuggingFaceEmbeddings(
    model_name = "intfloat/multilingual-e5-small",
    model_kwargs = {"device" : "cpu"},
    encode_kwargs = {"normalize_embeddings" : True}
)

PATH = os.path.dirname(__file__)
file_path = os.path.join(PATH,"curriculum_db")
computer_file_path = os.path.join(file_path,"computer_science")
humanitas_file_path = os.path.join(file_path,"humanitas")

if os.path.exists(os.path.join(PATH,"chroma_db")) :
    print("‼️ 벡터 DB가 이미 존재합니다. 삭제하고 업데이트할까요 ? ‼️")
    if input("[Y/N]").lower() == "n" :
        print("✅ 종료합니다.")
        exit()
    print("✅ DB를 업데이트합니다 !")
    shutil.rmtree(os.path.join(PATH,"chroma_db"))
    
header_splitters = [
    ("#", "header_1"),
    ("##", "header_2"),
    ("###", "header_3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=header_splitters)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

def process_folder(folder_path, category_name):
    documents = []
    
    if not os.path.exists(folder_path):
        print(f"⚠️ 폴더가 없습니다: {folder_path}")
        return documents

    files = os.listdir(folder_path)
    print(f"📂 {category_name} 폴더 처리 시작 ({len(files)}개 파일)")

    for file in files:
        if file.endswith(".txt") or not file.endswith(".md"): # .md 파일만 처리
            continue
            
        path = os.path.join(folder_path, file)
        
        # 1) 파일 읽기
        with open(path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        
        # 2) 헤더 기준 1차 분할
        header_splits = markdown_splitter.split_text(raw_text)
        
        # 3) 내용 길이 기준 2차 분할 및 메타데이터 주입
        for split in header_splits:
            if len(split.page_content) > 1000:
                final_splits = text_splitter.split_documents([split])
            else:
                final_splits = [split]
                
            # ✅ [수정됨] 들여쓰기를 안쪽으로 넣어서 모든 split을 처리하게 함
            for doc in final_splits:
                doc.page_content = f"passage: {doc.page_content}"
                doc.metadata["source"] = file
                doc.metadata["category"] = category_name
                documents.append(doc)
                
    print(f"   -> {len(documents)}개의 청크 생성 완료")
    return documents


computer_documents = process_folder(computer_file_path,"computer_science")
humanitas_documents = process_folder(humanitas_file_path,"humanitas")

computer_db = Chroma.from_documents(
    documents = computer_documents,
    embedding = embedding_function,
    persist_directory = os.path.join(PATH,"chroma_db"),
    collection_name = "computer_science",
    collection_metadata = {"hnsw:space" : "cosine"}
)

humanitas_db = Chroma.from_documents(
    documents = humanitas_documents,
    embedding = embedding_function,
    persist_directory = os.path.join(PATH,"chroma_db"),
    collection_name = "humanitas",
    collection_metadata = {"hnsw:space" : "cosine"}
)