import uuid

from app.schemas.task import TaskCreateRequest, TaskResponse


class TaskService:
    def create_task(self, payload: TaskCreateRequest) -> TaskResponse:
        return TaskResponse(
            id=str(uuid.uuid4()),
            title=payload.title,
            status="received",
            user_prompt=payload.user_prompt,
            sources=payload.sources,
        )
