from tortoise import Tortoise

async def init_db():
    await Tortoise.init(db_url='sqlite:////home/suny/agent/fapi/db.sqlite3',modules={'models': ['models']}, timezone='Asia/Shanghai')
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()