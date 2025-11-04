from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

model = ChatOllama(model = "gemma2:2b")

# print("------Prompt from Template------")
# template = "Tell me a joke about {topic}."
# prompt_template = ChatPromptTemplate.from_template(template)

# prompt = prompt_template.invoke({"topic" : "Cats"})
# result = model.invoke(prompt)
# print(result.content)

print("-----Prompt with Multiple Placeholders-----")
template_multiple = """You are a helpful assistant.
Human : Tell me a {adjactive} short story about a {animal}.
Assistant : """
prompt_template = ChatPromptTemplate.from_template(template_multiple)
prompt = prompt_template.invoke({"adjactive" : "funny", "animal" : "panda"})

result = model.invoke(prompt)
print(result.content)