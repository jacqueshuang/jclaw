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
