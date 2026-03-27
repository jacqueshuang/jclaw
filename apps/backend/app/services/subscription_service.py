class SubscriptionService:
    def can_submit(self, *, task_usage: int, task_quota: int) -> bool:
        return task_usage < task_quota
