import os,shutil
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_function = HuggingFaceEmbeddings(
    model_name = "intfloat/multilingual-e5-large",
    model_kwargs = {"device" : "cpu"},
    encode_kwargs = {"normalize_embeddings" : True}
)

PATH = os.path.dirname(__file__)
file_path = os.path.join(PATH,"curriculum_db")
computer_file_path = os.path.join(file_path,"computer_science")
humanitas_file_path = os.path.join(file_path,"humanitas")
computer_documents = []
humanitas_documents = []

if os.path.exists(os.path.join(PATH,"chroma_db")) :
    print("‼️ 벡터 DB가 이미 존재합니다. 삭제하고 업데이트할까요 ? ‼️")
    user_input = input("[Y/N]")
    if user_input.lower() == "n" :
        print("✅ 종료합니다.")
        exit()
    else :
        print("✅ DB를 업데이트합니다 !")
        shutil.rmtree(os.path.join(PATH,"chroma_db"))

computer_files = os.listdir(computer_file_path)

#컴공 교육과정 불러오기
for file in computer_files :
    loader = UnstructuredMarkdownLoader(os.path.join(computer_file_path,file))
    docs = loader.load()
    computer_documents.extend(docs)

humanitas_files = os.listdir(humanitas_file_path)

#교양 교육과정 불러오기
for file in humanitas_files :
    loader = UnstructuredMarkdownLoader(os.path.join(humanitas_file_path,file))
    docs = loader.load()
    humanitas_documents.extend(docs)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2000,
    chunk_overlap = 500
)

computer_documents = text_splitter.split_documents(computer_documents)
humanitas_documents = text_splitter.split_documents(humanitas_documents)

for doc in computer_documents :
    doc.page_content = f"passage: {doc.page_content}"

for doc in humanitas_documents :
    doc.page_content = f"passage: {doc.page_content}"

# 컴공 교육과정 vector db에 넣기
chroma_db = Chroma.from_documents(
    documents = computer_documents,
    embedding = embedding_function,
    persist_directory = os.path.join(PATH,"chroma_db"),
    collection_name = "computer_science",
    collection_metadata = {"hnsw:space" : "cosine"}
)

#교양 교육과정 vector db에 넣기
chroma_db = Chroma.from_documents(
    documents = humanitas_documents,
    embedding = embedding_function,
    persist_directory = os.path.join(PATH,"chroma_db"),
    collection_name = "humanitas",
    collection_metadata = {"hnsw:space" : "cosine"}
)