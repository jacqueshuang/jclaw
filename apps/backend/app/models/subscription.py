from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    plan_name: Mapped[str] = mapped_column(String(64))
    task_quota: Mapped[int] = mapped_column(Integer)
    task_usage: Mapped[int] = mapped_column(Integer, default=0)
