from app.core.database import SessionLocal
from app.jobs.celery_app import celery_app
from app.models.source import Source
from app.models.task import Task
from app.orchestration.contracts import SourceContent
from app.orchestration.delivery import DeliveryStage
from app.orchestration.research import ResearchStage
from app.orchestration.synthesis import SynthesisStage
from app.services.deliverable_service import DeliverableService
from app.services.knowledge_pack_service import KnowledgePackService


@celery_app.task(name="jclaw.tasks.run_task_pipeline")
def run_task_pipeline(task_id: str) -> str:
    with SessionLocal() as session:
        task = session.get(Task, task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")

        sources = [
            SourceContent(content=row.content)
            for row in session.query(Source).filter(Source.task_id == task_id).all()
        ]

        research = ResearchStage()
        synthesis = SynthesisStage()
        delivery = DeliveryStage()

        research_result = research.run(
            task_prompt=task.user_prompt,
            sources=sources,
        )
        synthesis_result = synthesis.run(research_result)
        deliverable = delivery.run(synthesis_result)

        KnowledgePackService().save(
            session,
            task_id=task_id,
            summary=synthesis_result.summary,
            outline=synthesis_result.outline,
        )
        DeliverableService().save(
            session,
            task_id=task_id,
            content_markdown=deliverable.content_markdown,
            content_type=deliverable.content_type,
        )

        task.status = "delivered"
        session.commit()

        return task_id
