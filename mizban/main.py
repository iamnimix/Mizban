import pathlib
import sys

from fastapi import FastAPI


ROOT_DIR = pathlib.Path(__file__).resolve()
sys.path.append(str(ROOT_DIR))

from .Routes.shortener.routes import router
from .Core.database import init_db

app = FastAPI()


app.include_router(router)


@app.on_event("startup")
async def startup_event():
    await init_db()
