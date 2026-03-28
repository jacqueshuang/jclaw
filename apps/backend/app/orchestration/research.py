from app.orchestration.contracts import ResearchResult, SourceContent


class ResearchStage:
    def run(self, *, task_prompt: str, sources: list[SourceContent]) -> ResearchResult:
        joined = "\n".join(source.content for source in sources)
        return ResearchResult(summary=f"{task_prompt}\n{joined}", source_titles=[])
