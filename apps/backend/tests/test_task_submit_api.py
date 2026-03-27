from sqlalchemy import text
from sqlalchemy.orm import Session


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
