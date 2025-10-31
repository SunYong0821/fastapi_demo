from tortoise import Tortoise

async def init_db():
    await Tortoise.init(db_url='postgres://ai:ai@localhost:5432/users',modules={'models': ['models']}, timezone='Asia/Shanghai')
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()