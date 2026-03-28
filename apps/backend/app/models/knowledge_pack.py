from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class KnowledgePack(Base):
    __tablename__ = "knowledge_packs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"), unique=True)
    summary: Mapped[str] = mapped_column(Text)
    outline: Mapped[str] = mapped_column(Text)
