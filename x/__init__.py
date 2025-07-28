import glob
import importlib
from fastapi import APIRouter

dirname = 'x'
def register_x(app):
    api_router = APIRouter()
    for module_file in glob.glob(f"{dirname}/[!_]*.py"):
        filename = module_file.split('/')[-1][:-3]
        module = importlib.import_module(f'{dirname}.{filename}')
        api_router.include_router(module.router)

    app.include_router(api_router)
