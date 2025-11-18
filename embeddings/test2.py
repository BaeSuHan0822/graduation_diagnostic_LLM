import os
import shutil
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

embedding_function = HuggingFaceEmbeddings(
    model_name = "intfloat/multilingual-e5-large",
    model_kwargs = {"device" : "cpu"},
    encode_kwargs = {"normalize_embeddings" : True}
)

PATH = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(PATH,"curriculum_db")
output_path = os.path.join(PATH,"chroma_db")
all_text = []

if os.path.exists(output_path) :
    print("벡터 DB가 이미 존재합니다. 덮어 씌울까요 ?")
    a = input("[Y/N]")
    if a.lower() == "n" :
        print("종료합니다.")
        exit()
    else :
        print("벡터 DB를 업데이트합니다...")
        shutil.rmtree(output_path)
            
else :
    print("새 벡터 DB를 생성합니다")
    
files = os.listdir(file_path)
        
for file in files :
    docs = TextLoader(os.path.join(file_path,file),encoding = "utf-8")
    docs = docs.load()
    all_text.extend(docs)
    
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2000,
    chunk_overlap = 500
)

splits = text_splitter.split_documents(all_text)

for split in splits :
    split.page_content = "passage: " + split.page_content
    
input = ["query: 컴퓨터공학과의 졸업학점은 몇 점이야 ?"]

vector_store = Chroma.from_documents(
    documents = splits,
    embedding= embedding_function,
    persist_directory= output_path,
    collection_metadata = {"hnsw:space" : "cosine"}
)

results = vector_store.similarity_search_with_score(input[0],k=3)

print("=== 검색 결과 ===")

for i,(doc,score) in enumerate(results) :
    content = doc.page_content.replace("passage: ","")
    
    print(f"{i+1}순위")
    print(f"유사도 거리(Score): {score:.4f}") 
    print(f"출처: {doc.metadata.get('source', '알 수 없음')}")
    print(f"내용: {content[:200]}...")
    print("-" * 50)