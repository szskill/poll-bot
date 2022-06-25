from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

web_app = FastAPI()
web_app.mount("/", StaticFiles(directory="bot/web/static", html=True), name="static")


@web_app.get("/")
async def index() -> str:
    return "Hello, world!"
