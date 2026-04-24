from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agents import build_whu_workflow, build_ksd_team

app = FastAPI()

class ChatRequest(BaseModel):
    username: str
    question: str
    enable_thinking: bool = False

class EventData(BaseModel):
    event: str
    step_name: str = None
    content: str = None

@app.post("/chatKSD")
async def chat_ksd(request: ChatRequest):
    try:
        team = build_ksd_team(enable_thinking=request.enable_thinking)
        async def event_stream():
            try:
                async for event in team.arun(input=request.question, user_id=request.username, stream=True, stream_events=True):
                    event_name = getattr(event, "event", type(event).__name__)
                    event_data = EventData(event=event_name)
                    if hasattr(event, "step_name"):
                        event_data.step_name = event.step_name
                    if hasattr(event, "content") and event.content:
                        event_data.content = event.content
                    yield f"data: {event_data.model_dump_json()}\n\n"
            except Exception as e:
                yield f"[ERROR] {str(e)}"
        return StreamingResponse(event_stream(), media_type="text/event-stream",headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            })
    except Exception as e:
        async def error_stream():
            yield f"[ERROR] 构建工作流失败: {str(e)}"
        return StreamingResponse(error_stream(), media_type="text/plain")

@app.post("/chatWHU")
async def chat_whu(request: ChatRequest):
    try:
        workflow = build_whu_workflow(enable_thinking=request.enable_thinking)
        async def event_stream():
            try:
                async for event in workflow.arun(input=request.question, user_id=request.username, stream=True, stream_events=True):
                    event_name = getattr(event, "event", type(event).__name__)
                    event_data = EventData(event=event_name)
                    if hasattr(event, "step_name"):
                        event_data.step_name = event.step_name
                    if hasattr(event, "content") and event.content:
                        event_data.content = event.content
                    yield f"data: {event_data.model_dump_json()}\n\n"
            except Exception as e:
                yield f"[ERROR] {str(e)}"
        return StreamingResponse(event_stream(), media_type="text/event-stream",headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            })
    except Exception as e:
        async def error_stream():
            yield f"[ERROR] 构建工作流失败: {str(e)}"
        return StreamingResponse(error_stream(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
