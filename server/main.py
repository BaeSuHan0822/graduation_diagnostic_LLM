from fastapi import FastAPI,UploadFile,File
import requests,tempfile,json
from fastapi.responses import FileResponse

app = FastAPI()

PARSER_URL = "http://localhost:9000/parse"
FRIENDLY_PARSER_URL = "http://localhost:7000/friendly"
LLM_URL = "http://llm-service:6000/inference"

@app.post("/upload")
def post_file(file : UploadFile = File(...)) :
    text = file.file.read().decode("cp949")
    text = text.replace("\r\n","\n").replace("\r","\n")
    
    nature_json = requests.post(PARSER_URL, json={"text" : text})
    nature_json = nature_json.json()
    
    friendly_text = requests.post(FRIENDLY_PARSER_URL,json=nature_json)
    friendly_text = friendly_text.text
    
    llm_response = requests.post(LLM_URL,data = friendly_text)
    llm_text = llm_response.text
    
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    with open(temp.name, "w", encoding="utf-8") as f:
        f.write(llm_text)

    return FileResponse(
        temp.name,
        media_type="text/plain",
        filename="graduation_result.txt"
    )

@app.get("/health")
def health() :
    return {"status" : "server ok"}