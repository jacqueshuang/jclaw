def fetch_url_content(url: str) -> str:
    """Return deterministic placeholder text for URL ingestion tests.

    This connector intentionally does not perform network I/O yet.
    """
    return f"[stub] URL content placeholder for {url}"
