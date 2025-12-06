
from fastapi import FastAPI
from .routers import users

app = FastAPI(title="ConnectNet")

app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "ConnectNet API is running"}
