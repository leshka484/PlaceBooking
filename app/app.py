from fastapi import FastAPI

from app.routers import main, users

app = FastAPI()

app.include_router(main.router)
app.include_router(users.router)