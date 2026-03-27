from app.services.subscription_service import SubscriptionService


def test_can_create_task_when_usage_is_below_quota() -> None:
    service = SubscriptionService()

    assert service.can_submit(task_usage=2, task_quota=3) is True


def test_cannot_create_task_when_usage_reaches_quota() -> None:
    service = SubscriptionService()

    assert service.can_submit(task_usage=3, task_quota=3) is False
