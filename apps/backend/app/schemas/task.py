from pydantic import BaseModel

from app.schemas.deliverable import DeliverableResponse
from app.schemas.knowledge_pack import KnowledgePackResponse
from app.schemas.source import SourceInput, SourceOutput


class TaskCreateRequest(BaseModel):
    title: str
    user_prompt: str
    sources: list[SourceInput]


class TaskResponse(BaseModel):
    id: str
    title: str
    status: str
    user_prompt: str
    sources: list[SourceOutput]


class TaskDetailResponse(TaskResponse):
    knowledge_pack: KnowledgePackResponse | None = None
    deliverable: DeliverableResponse | None = None
