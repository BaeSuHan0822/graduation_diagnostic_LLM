from fastapi import FastAPI,UploadFile,File
import requests,tempfile,json
from fastapi.responses import FileResponse

app = FastAPI()

PARSER_URL = "http://parser-service:9000/parse"

@app.post("/upload")
def post_file(file : UploadFile = File(...)) :
    text = file.file.read().decode("cp949")
    text = text.replace("\r\n","\n").replace("\r","\n")
    
    response = requests.post(PARSER_URL, json={"text" : text})
    result = response.json()
    
    temp = tempfile.NamedTemporaryFile(delete=False,suffix = "json")
    with open(temp.name, "w", encoding = "utf-8") as f :
        json.dump(result, f ,ensure_ascii = False, indent = 4)
        
    return FileResponse(
        temp.name,
        filename="parsed_result.json",
        media_type="applications/json"
    )

@app.get("/health")
def health() :
    return {"status" : "server ok"}