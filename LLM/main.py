from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from llm import diagnose_graduation 

app = FastAPI()

@app.post("/inference")
async def inference(request: Request):
    text = await request.body()
    text = text.decode("utf-8")

    try:
        result_text = diagnose_graduation(text)
    except Exception as e:
        return PlainTextResponse(
            content=f"LLM 처리 중 오류 발생: {str(e)}",
            status_code=500
        )

    return PlainTextResponse(content=result_text, status_code=200)


@app.get("/health")
def health():
    return {"status": "llm ok"}
