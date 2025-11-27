from fastapi import FastAPI,Request
from parser_logic import text_to_parsed_json

app = FastAPI()

@app.post("/parse")
async def parse_text(request : Request) :
    body = await request.json()
    text = body.get("text","")
    text = text.replace("\r\n","\n").replace("\r","\n")
    
    parsed_text = text_to_parsed_json(text)
    return parsed_text

@app.get("/health")
def health() :
    return {"status" : "ok"}