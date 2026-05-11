from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from context import lifespan
from auth import auth_middleware
import uvicorn

app = FastAPI(lifespan=lifespan)
# app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

# allow_credentials=True production env
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["GET", "POST"],allow_headers=["*"])
app.middleware("http")(auth_middleware)

@app.get("/")
async def root():
    return {"msg": "欢迎使用FastAPI"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    # uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=4)
