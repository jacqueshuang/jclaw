from pydantic import BaseModel


class KnowledgePackResponse(BaseModel):
    summary: str
    outline: str
