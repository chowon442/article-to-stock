import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from b import analyze
import uvicorn

app = FastAPI()

# 정적 파일 서비스
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.post("/api/analyze")
async def analyze_news(request: Request):
    data = await request.json()
    # 분석할 url
    url = data.get("url")
    result = analyze(url)
    if result == -1:
        return {"received_url": url, "status": "failed", "message": "LLM 분석 실패 또는 잘못된 응답입니다."}
    else:
        return {"received_url": url, "status": "success", "result": result}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)