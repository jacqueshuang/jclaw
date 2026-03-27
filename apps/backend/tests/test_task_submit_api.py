import uuid

import app.api.routes.deliverables as deliverables_routes
import app.models.deliverable  # noqa: F401
import app.models.knowledge_pack  # noqa: F401
import pytest
from fastapi import status
from sqlalchemy import event, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.deliverable import Deliverable
from app.models.knowledge_pack import KnowledgePack
from app.models.source import Source
from app.models.subscription import Subscription
from app.models.task import Task
from app.schemas.source import SourceOutput
from app.schemas.task import TaskCreateRequest, TaskDetailResponse, TaskResponse
from app.services.task_service import TaskService


@pytest.fixture
def seeded_delivered_task(db_session: Session) -> Task:
    task = Task(
        id=str(uuid.uuid4()),
        title="Seeded delivered task",
        status="delivered",
        user_prompt="Research browser agents",
    )
    db_session.add(task)
    db_session.commit()

    db_session.add(
        KnowledgePack(
            id=str(uuid.uuid4()),
            task_id=task.id,
            summary="Summary text",
            outline="- Point one",
        )
    )
    db_session.add(
        Deliverable(
            id=str(uuid.uuid4()),
            task_id=task.id,
            content_markdown="# Delivered article",
            content_type="article",
        )
    )
    db_session.commit()
    return task


def test_get_task_detail_returns_deliverable(client, seeded_delivered_task) -> None:
    response = client.get(f"/api/tasks/{seeded_delivered_task.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "delivered"
    assert body["deliverable"]["content_type"] == "article"
    assert body["knowledge_pack"]["summary"] != ""


def test_submit_task_creates_received_task(client) -> None:
    response = client.post(
        "/api/tasks",
        json={
            "title": "Write market overview",
            "user_prompt": "Research AI browser agents and write an article.",
            "sources": [
                {"source_type": "text", "title": "brief", "content": "Focus on 2026 products."}
            ],
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "received"
    assert body["title"] == "Write market overview"
    assert len(body["sources"]) == 1


def test_submit_task_persists_rows(client, db_session: Session) -> None:
    db_session.add(
        Subscription(
            id=str(uuid.uuid4()),
            plan_name="single-user",
            task_quota=3,
            task_usage=0,
        )
    )
    db_session.commit()

    response = client.post(
        "/api/tasks",
        json={
            "title": "Write market overview",
            "user_prompt": "Research AI browser agents and write an article.",
            "sources": [
                {"source_type": "text", "title": "brief", "content": "Focus on 2026 products."}
            ],
        },
    )

    assert response.status_code == 201
    assert db_session.execute(text("select count(*) from tasks")).scalar_one() == 1
    assert db_session.execute(text("select count(*) from sources")).scalar_one() == 1
    assert db_session.execute(text("select task_usage from subscriptions")).scalar_one() == 1


def test_request_commit_does_not_commit_pending_test_session_data(client, db_session: Session) -> None:
    db_session.add(
        Task(
            id=str(uuid.uuid4()),
            title="pending-test-task",
            status="received",
            user_prompt="pending",
        )
    )

    response = client.post(
        "/api/tasks",
        json={
            "title": "Write market overview",
            "user_prompt": "Research AI browser agents and write an article.",
            "sources": [
                {"source_type": "text", "title": "brief", "content": "Focus on 2026 products."}
            ],
        },
    )

    assert response.status_code == 201
    assert db_session.execute(text("select count(*) from tasks")).scalar_one() == 1


def test_sqlite_enforces_foreign_keys_in_tests(db_session: Session) -> None:
    db_session.add(
        Source(
            id=str(uuid.uuid4()),
            task_id=str(uuid.uuid4()),
            source_type="text",
            title="orphan",
            content="orphan",
        )
    )

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_deliverables_route_module_is_explicit_placeholder() -> None:
    assert not hasattr(deliverables_routes, "router")



def test_task_source_schema_split_for_read_models() -> None:
    sample = {
        "id": str(uuid.uuid4()),
        "title": "Write market overview",
        "status": "received",
        "user_prompt": "Research AI browser agents and write an article.",
        "sources": [{"source_type": "text", "title": "brief", "content": "Focus on 2026 products."}],
    }

    task_response = TaskResponse.model_validate(sample)
    task_detail_response = TaskDetailResponse.model_validate(sample)

    assert isinstance(task_response.sources[0], SourceOutput)
    assert isinstance(task_detail_response.sources[0], SourceOutput)



def test_task_service_returns_persisted_sources(db_session: Session) -> None:
    db_session.add(
        Subscription(
            id=str(uuid.uuid4()),
            plan_name="single-user",
            task_quota=3,
            task_usage=0,
        )
    )
    db_session.commit()

    service = TaskService()
    payload = TaskCreateRequest(
        title="Write market overview",
        user_prompt="Research AI browser agents and write an article.",
        sources=[
            {
                "source_type": "text",
                "title": "brief",
                "content": "Focus on 2026 products.",
            }
        ],
    )

    def mutate_source_before_flush(session: Session, _flush_context, _instances) -> None:
        for item in session.new:
            if isinstance(item, Source):
                item.title = "brief-from-db"

    event.listen(db_session, "before_flush", mutate_source_before_flush)
    try:
        response = service.create_task(db_session, payload)
    finally:
        event.remove(db_session, "before_flush", mutate_source_before_flush)

    assert response.sources[0].title == "brief-from-db"


def test_submit_task_rejects_when_subscription_quota_is_exhausted(
    client,
    db_session: Session,
) -> None:
    db_session.add(
        Subscription(
            id=str(uuid.uuid4()),
            plan_name="single-user",
            task_quota=1,
            task_usage=1,
        )
    )
    db_session.commit()

    response = client.post(
        "/api/tasks",
        json={
            "title": "Write market overview",
            "user_prompt": "Research AI browser agents and write an article.",
            "sources": [
                {"source_type": "text", "title": "brief", "content": "Focus on 2026 products."}
            ],
        },
    )

    assert response.status_code == status.HTTP_402_PAYMENT_REQUIRED
    assert response.json()["detail"] == "Task quota exceeded"
    assert db_session.execute(text("select count(*) from tasks")).scalar_one() == 0
