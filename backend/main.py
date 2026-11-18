
from fastapi import FastAPI

from backend.routers import users
from backend.routers import agents
from backend.routers import workflows
from backend.routers import tasks

from backend.database import Base, engine
from backend import models, agent_models, workflow_models,task_models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Agentic AI Platform",
    description="Enterprise Operations and Intelligent Automation API",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(agents.router)
app.include_router(workflows.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Enterprise Agentic AI Platform",
        "status": "Application is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
