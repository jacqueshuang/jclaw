import uuid

import app.models.deliverable  # noqa: F401
import app.models.knowledge_pack  # noqa: F401
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.jobs.tasks import run_task_pipeline
from app.models.source import Source
from app.models.task import Task
from app.orchestration.contracts import SourceContent
from app.orchestration.delivery import DeliveryStage
from app.orchestration.research import ResearchStage
from app.orchestration.synthesis import SynthesisStage


@pytest.fixture
def seeded_task(db_session: Session) -> Task:
    task = Task(
        id=str(uuid.uuid4()),
        title="Seeded task",
        status="received",
        user_prompt="Research browser agents",
    )
    db_session.add(task)
    db_session.commit()
    db_session.add(
        Source(
            id=str(uuid.uuid4()),
            task_id=task.id,
            source_type="text",
            title="Agent notes",
            content="Agent A",
        )
    )
    db_session.commit()
    return task


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


def test_run_task_pipeline_executes_orchestration_stages(monkeypatch, testing_session_local) -> None:
    session = testing_session_local()
    try:
        task = Task(
            id=str(uuid.uuid4()),
            title="Task",
            status="received",
            user_prompt="Research browser agents",
        )
        session.add(task)
        session.commit()
        session.add(
            Source(
                id=str(uuid.uuid4()),
                task_id=task.id,
                source_type="text",
                title="source",
                content="Task source",
            )
        )
        session.commit()

        monkeypatch.setattr("app.jobs.tasks.SessionLocal", testing_session_local, raising=False)

        result = run_task_pipeline(task.id)

        assert result == task.id
    finally:
        session.close()


def test_run_task_pipeline_persists_knowledge_pack_and_deliverable(
    db_session: Session,
    seeded_task: Task,
    monkeypatch,
    testing_session_local,
) -> None:
    monkeypatch.setattr("app.jobs.tasks.SessionLocal", testing_session_local, raising=False)

    run_task_pipeline(seeded_task.id)

    assert db_session.execute(text("select count(*) from knowledge_packs")).scalar_one() == 1
    assert db_session.execute(text("select count(*) from deliverables")).scalar_one() == 1
