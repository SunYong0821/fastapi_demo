from contextlib import asynccontextmanager
from database import init_db, close_db
from api import register_api
from x import register_x

@asynccontextmanager
async def lifespan(app):
    await init_db()
    register_api(app)
    register_x(app)
    
    yield
    
    await close_db()

