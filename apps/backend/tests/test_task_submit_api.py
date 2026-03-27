import uuid

import pytest
from sqlalchemy import event, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.source import Source
from app.models.task import Task
from app.schemas.task import TaskCreateRequest
from app.services.task_service import TaskService


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


def test_task_service_returns_persisted_sources(db_session: Session) -> None:
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
