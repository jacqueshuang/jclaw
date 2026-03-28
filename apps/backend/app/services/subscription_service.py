from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.subscription import Subscription


class SubscriptionService:
    MVP_PLAN_NAME = "single-user"

    def can_submit(self, *, task_usage: int, task_quota: int) -> bool:
        return task_usage < task_quota

    def get_mvp_subscription(self, session: Session) -> Subscription | None:
        return session.scalars(
            select(Subscription)
            .where(Subscription.plan_name == self.MVP_PLAN_NAME)
            .order_by(Subscription.id)
        ).first()

    def claim_task_slot(self, session: Session, *, subscription_id: str) -> bool:
        result = session.execute(
            update(Subscription)
            .where(Subscription.id == subscription_id)
            .where(Subscription.task_usage < Subscription.task_quota)
            .values(task_usage=Subscription.task_usage + 1)
        )
        return result.rowcount == 1
