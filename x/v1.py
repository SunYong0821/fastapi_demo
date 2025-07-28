from fastapi import APIRouter, Request

router = APIRouter(prefix="/v1", tags=["LLM"])

@router.get("/")
async def llm():
    return {"status_code": 200, "msg": 'LLM test'}

