from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.ai_ml.task_classifier import task_classifier

router = APIRouter(
    prefix="/ai-ml",
    tags=["AI/ML"]
)


class TaskPredictionRequest(BaseModel):
    task_description: str


@router.post("/predict")
def predict_task(request: TaskPredictionRequest):

    if not request.task_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Task description cannot be empty"
        )

    try:
        prediction = task_classifier.predict(
            request.task_description
        )

        return {
            "task_description": request.task_description,
            "predicted_category": prediction,
            "message": "Task category predicted successfully"
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )