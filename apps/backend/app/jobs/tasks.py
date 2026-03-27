from app.jobs.celery_app import celery_app


@celery_app.task(name="run_task_pipeline")
def run_task_pipeline(task_id: str) -> str:
    return task_id
