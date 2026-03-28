from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.deliverable import Deliverable
from app.schemas.deliverable import DeliverableResponse

router = APIRouter(prefix="/api/deliverables", tags=["deliverables"])


@router.get("/{task_id}", response_model=DeliverableResponse)
def get_deliverable(task_id: str, db: Session = Depends(get_db)) -> DeliverableResponse:
    deliverable = db.scalars(select(Deliverable).where(Deliverable.task_id == task_id)).one_or_none()
    if deliverable is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deliverable not found")

    return DeliverableResponse(
        content_markdown=deliverable.content_markdown,
        content_type=deliverable.content_type,
    )
