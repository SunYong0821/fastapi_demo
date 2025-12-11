from tortoise import Tortoise

async def init_db():
    await Tortoise.init(db_url='postgres://ai:ai@localhost:5432/xxx',modules={'models': ['models']}, timezone='Asia/Shanghai')
    await Tortoise.generate_schemas(safe=True)

async def close_db():
    await Tortoise.close_connections()