from app.orchestration.delivery import DeliveryStage
from app.orchestration.research import ResearchStage
from app.orchestration.synthesis import SynthesisStage


def test_pipeline_transforms_task_into_deliverable() -> None:
    research = ResearchStage()
    synthesis = SynthesisStage()
    delivery = DeliveryStage()

    research_result = research.run(task_prompt="Research browser agents", sources=[{"content": "Agent A"}])
    synthesis_result = synthesis.run(research_result)
    deliverable = delivery.run(synthesis_result)

    assert "Agent A" in research_result.summary
    assert synthesis_result.summary != ""
    assert deliverable.content_markdown.startswith("#")
