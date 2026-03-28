from app.orchestration.contracts import DeliverableResult, SynthesisResult


class DeliveryStage:
    def run(self, synthesis_result: SynthesisResult) -> DeliverableResult:
        return DeliverableResult(content_markdown=f"# Draft\n\n{synthesis_result.summary}")
