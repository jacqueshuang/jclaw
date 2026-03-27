from pydantic import BaseModel


class SourceInput(BaseModel):
    """Normalized source payload accepted by Task 4 task intake."""

    source_type: str
    title: str
    content: str
