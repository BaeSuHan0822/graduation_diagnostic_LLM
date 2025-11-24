import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM

current_dir = os.path.dirnmae(__file__)
persist_directory = os.path.join(current_dir,"chroma_db")

embedding_function = HuggingFaceEmbeddings(
    model_name = "intfloat/multilingual-e5-large",
    model_kwargs = {"device" : "cpu"},
    encode_kwargs = {"normalize_embeddings" : True}
)

computer_db = Chroma(
    persist_directory = persist_directory,
    embedding_function = embedding_function,
    collection_name = "computer_science"
)

humanitas_db = Chroma(
    persist_directory = persist_directory,
    embedding_function = embedding_function,
    collection_name = "humanitas"
)

user_query = "query: 컴퓨터공학과를 졸업하기 위해서 필요한 전공학점과 교양학점은 ?"

computer_result = computer_db.similarity_search_with_score(user_query[0],k = 4)
humanitas_result = humanitas_db.similarity_search_with_score(user_query[0],k =2)

result = sorted(computer_result + humanitas_result,key = lambda x: x[1])

text = ""
for index,(document,score) in enumerate(result) :
    text += f"Document {index+1}"
    text += document.page_content


tokenizer = AutoTokenizer.from_pretrained("kakaocorp/kanana-1.5-8b-instruct-2505")
model = AutoModelForCausalLM.from_pretrained("kakaocorp/kanana-1.5-8b-instruct-2505")
messages = [
    {"role": "user", "content": "Who are you?"},
]
inputs = tokenizer.apply_chat_template(
	messages,
	add_generation_prompt=True,
	tokenize=True,
	return_dict=True,
	return_tensors="pt",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=40)
print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]))
