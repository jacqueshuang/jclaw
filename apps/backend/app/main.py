from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.sources import router as sources_router
from app.api.routes.tasks import router as tasks_router

app = FastAPI(title="Jclaw Backend")
app.include_router(health_router)
app.include_router(tasks_router)
app.include_router(sources_router)
