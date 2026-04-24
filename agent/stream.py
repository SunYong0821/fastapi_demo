from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import json

class EventData(BaseModel):
    event: str
    step_name: str = None
    content: str = None

    @classmethod
    def from_source(cls, event_obj):
        return cls(
            event=getattr(event_obj, "event", type(event_obj).__name__),
            step_name=getattr(event_obj, "step_name", None),
            content=getattr(event_obj, "content", None)
        )

def stream_runnable(runnable, question: str, username: str) -> StreamingResponse:
    async def event_generator():
        try:
            async for event in runnable.arun(input=question, user_id=username, stream=True, stream_events=True):
                data = EventData.from_source(event)
                yield f"data: {data.model_dump_json()}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({"error": str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )