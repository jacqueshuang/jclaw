from pydantic import BaseModel


class DeliverableResponse(BaseModel):
    content_markdown: str
    content_type: str
