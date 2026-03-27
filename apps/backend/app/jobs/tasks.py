from app.jobs.celery_app import celery_app
from app.orchestration.delivery import DeliveryStage
from app.orchestration.contracts import SourceContent
from app.orchestration.research import ResearchStage
from app.orchestration.synthesis import SynthesisStage


@celery_app.task(name="jclaw.tasks.run_task_pipeline")
def run_task_pipeline(task_id: str) -> str:
    research = ResearchStage()
    synthesis = SynthesisStage()
    delivery = DeliveryStage()

    research_result = research.run(
        task_prompt=f"Task {task_id}",
        sources=[SourceContent(content=f"Task source {task_id}")],
    )
    synthesis_result = synthesis.run(research_result)
    deliverable = delivery.run(synthesis_result)

    return deliverable.content_markdown
