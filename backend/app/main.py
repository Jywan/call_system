from fastapi import FastAPI
from app.core.database import Base, engine

# 모델 import
from app.models.agent import Agent
from app.models.call_log import CallLog

# 라우터
from app.routers.agent_router import router as agent_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(agent_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}