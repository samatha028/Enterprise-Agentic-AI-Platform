from fastapi import FastAPI

from backend.routers import users

app = FastAPI(
    title="Enterprise Agentic AI Platform",
    description="Enterprise Operations and Intelligent Automation API",
    version="1.0.0"
)

app.include_router(users.router)


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