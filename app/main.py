from fastapi import FastAPI
from .database import engine
from .models import Base

app = FastAPI(title="TV Broadcasting API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok"}

