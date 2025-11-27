import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

current_dir = os.path.dirname(__file__)
persist_directory = os.path.join(current_dir,"chroma_db")

with open(os.path.join(current_dir,"student_db"),"r",encoding = "utf-8") as f :
    f.read()

print("✅ 모델 불러오기")
embedding_function = HuggingFaceEmbeddings(
    model_name = "intfloat/multilingual-e5-large",
    model_kwargs = {"device" : "cpu"},
    encode_kwargs = {"normalize_embeddings" : True}
)
print("✅ 컴퓨터공학과 Vector DB 불러오기 !")
computer_db = Chroma(
    persist_directory = persist_directory,
    embedding_function = embedding_function,
    collection_name = "computer_science"
)
print("✅ 성공 !")
print("✅ 교양 Vector DB 불러오기 !")
humanitas_db = Chroma(
    persist_directory = persist_directory,
    embedding_function = embedding_function,
    collection_name = "humanitas"
)
print("✅ 성공")

user_query = "컴퓨터공학과의 졸업전공학점"
search_query = f"query: {user_query}"

computer_result = computer_db.similarity_search_with_score(search_query,k = 4)
humanitas_result = humanitas_db.similarity_search_with_score(search_query,k =2)

result = sorted(computer_result + humanitas_result,key = lambda x: x[1])

text = ""
for index,(document,score) in enumerate(result) :
    text += f"Document {index+1}"
    text += document.page_content

llm = ChatOllama(
    model="gemma2:2b",
    temperture=0.1
)

template = """
당신은 꼼꼼한 대학교 학사 행정 도우미 AI입니다.
반드시 아래 [참고 문서] 중에서 찾아서 답변하고 모르는 것은 확실하게 모른다고 하세요.

답변할 때는 단순히 총 학점만 말하지 말고, 아래 항목을 포함하여 자세히 설명하세요:
- 총 졸업 이수 학점
- 전공 이수 학점 (기초, 필수, 선택 등 세부 내역 포함)
- 기타 중요 요건

[참고 문서]
{context}

[질문]
{question}

답변:
"""

prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    {"context": lambda x: text, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("🤖 Gemma2 AI 답변:")

# 스트리밍 출력 (타자 치듯 나옴)
for chunk in rag_chain.stream(user_query):
    print(chunk, end="", flush=True)

print("\n" + "="*50)