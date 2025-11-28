from fastapi import FastAPI

from Routes.shortener.routes import router
from Core.database import init_db

app = FastAPI()


app.include_router(router)


@app.on_event("startup")
async def startup_event():
    await init_db()
