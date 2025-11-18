### 이 코드는 사용하지 않습니다

import os
from Kanana import Custom_Kanana
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever

model = Custom_Kanana()
PATH = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(PATH,"curriculum_db")
output_path = os.path.join(PATH,"chroma_db")

docs_for_bm25 = []

if os.path.exists(output_path) :
    print("이미 존재합니다.")
else :
    os.makedirs(output_path)
    files = os.listdir(file_path)

    all_texts = []
    for file in files :
        loader = TextLoader(os.path.join(file_path,file))
        loader = loader.load()
        
        pages = [page.page_content for page in loader]
        text = "\n".join(pages)
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 3000,
            chunk_overlap = 500,
            separators = [".","?","!","\n"]
        )
        
        sentences = splitter.split_text(text)
        all_texts.extend(sentences)
        
        for chunk in sentences :
            docs_for_bm25.append(Document(page_content=chunk))
        
    vector_store = Chroma(
        collection_name = "curriculum_db",
        embedding_function = model,
        persist_directory= output_path
    )
    BATCH = 50

    for i in range(0,len(all_texts),BATCH) :
        batch_text = all_texts[i:i+BATCH]
        vector_store.add_texts(batch_text)
        


vector_store = Chroma(
        collection_name = "curriculum_db",
        embedding_function = model,
        persist_directory= output_path
    )  


semantic_retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs = {"k":5}
)

keyword_retriever = BM25Retriever.from_documents(docs_for_bm25)
keyword_retriever.k = 5

def hybrid_search(query):
    bm25_results = keyword_retriever._get_relevant_documents(query)
    semantic_results = semantic_retriever._get_relevant_documents(query)
    combined = bm25_results + semantic_results
    unique = {doc.page_content: doc for doc in combined}.values()
    return list(unique)

# (5) 검색 테스트
query = "컴퓨터공학과 22학번 전공선택 학점은?"
results = hybrid_search(query)

for i, doc in enumerate(results[:5]):
    print(f"\n=== Result {i+1} ===")
    print(doc.page_content[:300])