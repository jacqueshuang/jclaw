from app.orchestration.contracts import ResearchResult, SynthesisResult


class SynthesisStage:
    def run(self, research_result: ResearchResult) -> SynthesisResult:
        return SynthesisResult(summary=research_result.summary, outline="- intro\n- body\n- conclusion")
