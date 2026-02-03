from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

from core.graph.builder import run_graph
from .config import templates


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.post("/chat", response_class=JSONResponse)
async def chat_endpoint(request: Request):
    try:
        body = await request.json()
        prompt = body.get("prompt")
        if prompt is None or prompt.strip() == "":
            return {"error": "prompt is required"}
        prompt = body["prompt"]

        print(f"Received prompt: {prompt}")

        answer = run_graph(prompt)

        return {"answer": answer}
    except Exception as e:
        print(f"Error processing prompt: {str(e)}")
        return {"error": str(e)}
