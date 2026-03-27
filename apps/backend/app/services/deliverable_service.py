import uuid

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
        session.add(
            Deliverable(
                id=str(uuid.uuid4()),
                task_id=task_id,
                content_markdown=content_markdown,
                content_type=content_type,
            )
        )
