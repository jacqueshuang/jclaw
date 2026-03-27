from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.deliverable import Deliverable
from app.models.knowledge_pack import KnowledgePack
from app.models.source import Source
from app.models.task import Task
from app.schemas.deliverable import DeliverableResponse
from app.schemas.knowledge_pack import KnowledgePackResponse
from app.schemas.source import SourceInput
from app.schemas.task import TaskCreateRequest, TaskDetailResponse, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])
service = TaskService()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateRequest, db: Session = Depends(get_db)) -> TaskResponse:
    return service.create_task(db, payload)


@router.get("/{task_id}", response_model=TaskDetailResponse)
def get_task(task_id: str, db: Session = Depends(get_db)) -> TaskDetailResponse:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    sources = db.scalars(select(Source).where(Source.task_id == task_id).order_by(Source.id)).all()
    pack = db.scalars(select(KnowledgePack).where(KnowledgePack.task_id == task_id)).one_or_none()
    deliverable = db.scalars(select(Deliverable).where(Deliverable.task_id == task_id)).one_or_none()

    return TaskDetailResponse(
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
            for source in sources
        ],
        knowledge_pack=(
            None
            if pack is None
            else KnowledgePackResponse(summary=pack.summary, outline=pack.outline)
        ),
        deliverable=(
            None
            if deliverable is None
            else DeliverableResponse(
                content_markdown=deliverable.content_markdown,
                content_type=deliverable.content_type,
            )
        ),
    )
