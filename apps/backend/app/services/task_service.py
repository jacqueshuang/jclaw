import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.source import Source
from app.models.task import Task
from app.schemas.source import SourceOutput
from app.schemas.task import TaskCreateRequest, TaskResponse
from app.services.subscription_service import SubscriptionService


class TaskService:
    def create_task(self, session: Session, payload: TaskCreateRequest) -> TaskResponse:
        subscription_service = SubscriptionService()
        subscription = subscription_service.get_mvp_subscription(session)

        if subscription is not None and not subscription_service.claim_task_slot(
            session,
            subscription_id=subscription.id,
        ):
            session.rollback()
            raise HTTPException(status_code=402, detail="Task quota exceeded")

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
                SourceOutput(
                    source_type=source.source_type,
                    title=source.title,
                    content=source.content,
                )
                for source in persisted_sources
            ],
        )
