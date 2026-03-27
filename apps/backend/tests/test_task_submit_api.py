from fastapi.testclient import TestClient

from app.main import app


def test_submit_task_creates_received_task() -> None:
    client = TestClient(app)

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
