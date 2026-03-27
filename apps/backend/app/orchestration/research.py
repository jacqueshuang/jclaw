from app.orchestration.contracts import ResearchResult


class ResearchStage:
    def run(self, *, task_prompt: str, sources: list[dict[str, str]]) -> ResearchResult:
        joined = "\n".join(item["content"] for item in sources)
        return ResearchResult(summary=f"{task_prompt}\n{joined}", source_titles=[])
