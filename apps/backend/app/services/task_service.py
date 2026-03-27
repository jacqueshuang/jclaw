import uuid

from sqlalchemy.orm import Session

from app.models.source import Source
from app.models.task import Task
from app.schemas.task import TaskCreateRequest, TaskResponse


class TaskService:
    def create_task(self, session: Session, payload: TaskCreateRequest) -> TaskResponse:
        task = Task(
            id=str(uuid.uuid4()),
            title=payload.title,
            status="received",
            user_prompt=payload.user_prompt,
        )
        session.add(task)

        for item in payload.sources:
            session.add(
                Source(
                    id=str(uuid.uuid4()),
                    task_id=task.id,
                    source_type=item.source_type,
                    title=item.title,
                    content=item.content,
                )
            )

        session.commit()

        return TaskResponse(
            id=task.id,
            title=task.title,
            status=task.status,
            user_prompt=task.user_prompt,
            sources=payload.sources,
        )
