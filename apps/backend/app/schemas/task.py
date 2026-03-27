from pydantic import BaseModel

from app.schemas.source import SourceInput


class TaskCreateRequest(BaseModel):
    title: str
    user_prompt: str
    sources: list[SourceInput]


class TaskResponse(BaseModel):
    id: str
    title: str
    status: str
    user_prompt: str
    sources: list[SourceInput]
