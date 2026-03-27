import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.source import Source
from app.models.task import Task
from app.schemas.source import SourceInput
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
        session.flush()

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

        persisted_sources = session.scalars(
            select(Source).where(Source.task_id == task.id).order_by(Source.id)
        ).all()

        return TaskResponse(
            id=task.id,
            title=task.title,
            status=task.status,
            user_prompt=task.user_prompt,
            sources=[
                SourceInput(
                    source_type=source.source_type,
                    title=source.title,
                    content=source.content,
                )
                for source in persisted_sources
            ],
        )
