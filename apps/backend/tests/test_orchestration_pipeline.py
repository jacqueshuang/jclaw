from app.jobs.tasks import run_task_pipeline
from app.orchestration.contracts import SourceContent
from app.orchestration.delivery import DeliveryStage
from app.orchestration.research import ResearchStage
from app.orchestration.synthesis import SynthesisStage


def test_pipeline_transforms_task_into_deliverable() -> None:
    research = ResearchStage()
    synthesis = SynthesisStage()
    delivery = DeliveryStage()

    research_result = research.run(
        task_prompt="Research browser agents",
        sources=[SourceContent(content="Agent A")],
    )
    synthesis_result = synthesis.run(research_result)
    deliverable = delivery.run(synthesis_result)

    assert "Agent A" in research_result.summary
    assert synthesis_result.summary != ""
    assert deliverable.content_markdown.startswith("#")


def test_run_task_pipeline_executes_orchestration_stages() -> None:
    task_id = "task-123"

    result = run_task_pipeline(task_id)

    assert result.startswith("# Draft")
    assert f"Task source {task_id}" in result
