from fastapi import FastAPI
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Call System Backend")

@app.get("/health")
def health_check():
    return {"status": "ok"}