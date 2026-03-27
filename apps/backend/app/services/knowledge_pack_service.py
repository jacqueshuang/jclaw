import uuid

from sqlalchemy.orm import Session

from app.models.knowledge_pack import KnowledgePack


class KnowledgePackService:
    def save(self, session: Session, *, task_id: str, summary: str, outline: str) -> None:
        session.add(
            KnowledgePack(
                id=str(uuid.uuid4()),
                task_id=task_id,
                summary=summary,
                outline=outline,
            )
        )
