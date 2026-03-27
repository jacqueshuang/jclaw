from app.services.source_service import SourceService


def test_normalize_text_source() -> None:
    service = SourceService()

    source = service.normalize_text(title="brief", content="Market focus")

    assert source["source_type"] == "text"
    assert source["title"] == "brief"
    assert source["content"] == "Market focus"


def test_normalize_url_source(monkeypatch) -> None:
    service = SourceService()
    monkeypatch.setattr(service, "fetch_url", lambda url: "Fetched page")

    source = service.normalize_url(url="https://example.com")

    assert source["source_type"] == "web"
    assert source["content"] == "Fetched page"


def test_ingest_url_route_is_registered(client, monkeypatch) -> None:
    from app.api.routes import sources as sources_routes

    monkeypatch.setattr(
        sources_routes.service,
        "fetch_url",
        lambda url: "Stub web content",
    )

    response = client.post("/api/sources/url", json={"url": "https://example.com"})

    assert response.status_code == 200
    assert response.json() == {
        "source_type": "web",
        "title": "https://example.com",
        "content": "Stub web content",
    }
