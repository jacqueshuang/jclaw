from pydantic import BaseModel


class SourceInput(BaseModel):
    source_type: str
    title: str
    content: str
