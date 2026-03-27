from dataclasses import dataclass


@dataclass
class ResearchResult:
    summary: str
    source_titles: list[str]


@dataclass
class SynthesisResult:
    summary: str
    outline: str


@dataclass
class DeliverableResult:
    content_markdown: str
    content_type: str = "article"
