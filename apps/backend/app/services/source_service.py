from app.connectors.web import fetch_url_content


class SourceService:
    def normalize_text(self, *, title: str, content: str) -> dict[str, str]:
        return {"source_type": "text", "title": title, "content": content}

    def fetch_url(self, url: str) -> str:
        return fetch_url_content(url)

    def normalize_url(self, *, url: str) -> dict[str, str]:
        return {
            "source_type": "web",
            "title": url,
            "content": self.fetch_url(url),
        }
