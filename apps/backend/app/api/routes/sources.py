from fastapi import APIRouter
from pydantic import BaseModel

from app.services.source_service import SourceService

router = APIRouter(prefix="/api/sources", tags=["sources"])
service = SourceService()


class UrlIngestRequest(BaseModel):
    url: str


@router.post("/url")
def ingest_url(payload: UrlIngestRequest) -> dict[str, str]:
    return service.normalize_url(url=payload.url)
