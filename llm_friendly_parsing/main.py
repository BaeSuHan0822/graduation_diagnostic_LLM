from fastapi import FastAPI,Response
import llm_friendly_parsing as parsing

app = FastAPI()

@app.post("/friendly")
def friendly(payload: dict):
    friendly_text = parsing.generate_llm_friendly_text(payload)
    return Response(content=friendly_text, media_type="text/plain")