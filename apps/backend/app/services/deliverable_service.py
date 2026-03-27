import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.deliverable import Deliverable


class DeliverableService:
    def save(
        self,
        session: Session,
        *,
        task_id: str,
        content_markdown: str,
        content_type: str,
    ) -> None:
        existing = session.execute(
            select(Deliverable).where(Deliverable.task_id == task_id)
        ).scalar_one_or_none()

        if existing is None:
            session.add(
                Deliverable(
                    id=str(uuid.uuid4()),
                    task_id=task_id,
                    content_markdown=content_markdown,
                    content_type=content_type,
                )
            )
            return

        existing.content_markdown = content_markdown
        existing.content_type = content_type
