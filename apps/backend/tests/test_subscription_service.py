import uuid

from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.services.subscription_service import SubscriptionService


def test_can_create_task_when_usage_is_below_quota() -> None:
    service = SubscriptionService()

    assert service.can_submit(task_usage=2, task_quota=3) is True


def test_cannot_create_task_when_usage_reaches_quota() -> None:
    service = SubscriptionService()

    assert service.can_submit(task_usage=3, task_quota=3) is False


def test_select_mvp_subscription_prefers_single_user_plan_name(db_session: Session) -> None:
    db_session.add(
        Subscription(
            id=str(uuid.uuid4()),
            plan_name="starter",
            task_quota=99,
            task_usage=0,
        )
    )
    expected = Subscription(
        id="00000000-0000-0000-0000-000000000001",
        plan_name="single-user",
        task_quota=3,
        task_usage=1,
    )
    db_session.add(expected)
    db_session.add(
        Subscription(
            id="00000000-0000-0000-0000-000000000002",
            plan_name="single-user",
            task_quota=5,
            task_usage=0,
        )
    )
    db_session.commit()

    service = SubscriptionService()

    selected = service.get_mvp_subscription(db_session)

    assert selected is not None
    assert selected.id == expected.id


def test_claim_task_slot_is_atomic_for_quota(db_session: Session) -> None:
    subscription = Subscription(
        id=str(uuid.uuid4()),
        plan_name="single-user",
        task_quota=1,
        task_usage=0,
    )
    db_session.add(subscription)
    db_session.commit()

    service = SubscriptionService()

    assert service.claim_task_slot(db_session, subscription_id=subscription.id) is True
    assert service.claim_task_slot(db_session, subscription_id=subscription.id) is False

    refreshed = db_session.get(Subscription, subscription.id)
    assert refreshed is not None
    assert refreshed.task_usage == 1
