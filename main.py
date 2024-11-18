from fastapi import FastAPI

from src.routes.auth import router as auth_router
from src.routes.contacts import router as contact_router

app = FastAPI()

app.include_router(auth_router, prefix="/api")
app.include_router(contact_router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

