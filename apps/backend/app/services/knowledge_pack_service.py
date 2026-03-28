import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.knowledge_pack import KnowledgePack


class KnowledgePackService:
    def save(self, session: Session, *, task_id: str, summary: str, outline: str) -> None:
        existing = session.execute(
            select(KnowledgePack).where(KnowledgePack.task_id == task_id)
        ).scalar_one_or_none()

        if existing is None:
            session.add(
                KnowledgePack(
                    id=str(uuid.uuid4()),
                    task_id=task_id,
                    summary=summary,
                    outline=outline,
                )
            )
            return

        existing.summary = summary
        existing.outline = outline
