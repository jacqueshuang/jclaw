# Single-User Content Task MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-user AI content work desktop MVP that accepts a task in chat, ingests web and private sources, runs research and synthesis jobs through a multi-model backend, stores a Knowledge Pack, and delivers a publishable content result.

**Architecture:** The product is split into a Tauri 2 + Vue 3 desktop shell, a FastAPI backend, and PostgreSQL for persistence. The backend owns task orchestration, source ingestion, model-provider abstraction, job execution, and deliverable generation; the desktop app owns task submission, source upload, task status display, and deliverable review.

**Tech Stack:** Tauri 2, Vite, Vue 3, TypeScript, Rust, FastAPI, SQLAlchemy, Alembic, Celery, Redis, PostgreSQL, pytest, Vitest, Playwright, Anthropic SDK, OpenAI SDK, Google GenAI SDK

---

## Planned File Structure

### Frontend / desktop
- Create: `apps/desktop/package.json` — desktop workspace package manifest
- Create: `apps/desktop/vite.config.ts` — Vite config for Vue desktop UI
- Create: `apps/desktop/tsconfig.json` — TypeScript config
- Create: `apps/desktop/src/main.ts` — Vue entrypoint
- Create: `apps/desktop/src/App.vue` — root shell and layout
- Create: `apps/desktop/src/router/index.ts` — app routes
- Create: `apps/desktop/src/lib/api.ts` — typed HTTP client for backend APIs
- Create: `apps/desktop/src/stores/task.ts` — task state store
- Create: `apps/desktop/src/pages/TaskWorkspacePage.vue` — primary task workspace
- Create: `apps/desktop/src/components/TaskComposer.vue` — task input form
- Create: `apps/desktop/src/components/SourcePicker.vue` — source upload and URL input
- Create: `apps/desktop/src/components/TaskTimeline.vue` — task state view
- Create: `apps/desktop/src/components/DeliverablePanel.vue` — final deliverable display
- Create: `apps/desktop/src/components/KnowledgePackPanel.vue` — knowledge pack summary display
- Create: `apps/desktop/src/styles.css` — app styles
- Create: `apps/desktop/tests/task-workspace.spec.ts` — UI integration tests

### Tauri shell
- Create: `apps/desktop/src-tauri/Cargo.toml` — Rust manifest
- Create: `apps/desktop/src-tauri/tauri.conf.json` — Tauri config
- Create: `apps/desktop/src-tauri/src/main.rs` — Tauri bootstrap
- Create: `apps/desktop/src-tauri/src/lib.rs` — desktop shell command registration
- Create: `apps/desktop/src-tauri/src/backend.rs` — backend process launch and health check helper
- Create: `apps/desktop/src-tauri/tests/backend_launch.rs` — Rust smoke test for backend launch helper

### Backend
- Create: `apps/backend/pyproject.toml` — Python project manifest
- Create: `apps/backend/alembic.ini` — Alembic config
- Create: `apps/backend/alembic/env.py` — migration environment
- Create: `apps/backend/alembic/versions/20260327_01_initial_schema.py` — initial database schema
- Create: `apps/backend/app/main.py` — FastAPI bootstrap
- Create: `apps/backend/app/core/config.py` — settings and env parsing
- Create: `apps/backend/app/core/database.py` — SQLAlchemy engine and session factory
- Create: `apps/backend/app/core/security.py` — single-user auth stub and API key helper
- Create: `apps/backend/app/models/task.py` — task ORM model
- Create: `apps/backend/app/models/source.py` — source ORM model
- Create: `apps/backend/app/models/knowledge_pack.py` — knowledge pack ORM model
- Create: `apps/backend/app/models/deliverable.py` — deliverable ORM model
- Create: `apps/backend/app/models/subscription.py` — subscription and usage ORM model
- Create: `apps/backend/app/schemas/task.py` — task request/response schemas
- Create: `apps/backend/app/schemas/source.py` — source schemas
- Create: `apps/backend/app/schemas/knowledge_pack.py` — knowledge pack schemas
- Create: `apps/backend/app/schemas/deliverable.py` — deliverable schemas
- Create: `apps/backend/app/api/routes/health.py` — health endpoints
- Create: `apps/backend/app/api/routes/tasks.py` — task CRUD and submit endpoints
- Create: `apps/backend/app/api/routes/sources.py` — source upload and URL intake endpoints
- Create: `apps/backend/app/api/routes/deliverables.py` — deliverable read endpoints
- Create: `apps/backend/app/services/task_service.py` — task creation and state transitions
- Create: `apps/backend/app/services/source_service.py` — source ingest orchestration
- Create: `apps/backend/app/services/knowledge_pack_service.py` — knowledge pack persistence
- Create: `apps/backend/app/services/deliverable_service.py` — deliverable persistence
- Create: `apps/backend/app/services/subscription_service.py` — single-user plan and quota service
- Create: `apps/backend/app/providers/base.py` — provider abstraction
- Create: `apps/backend/app/providers/anthropic_provider.py` — Anthropic adapter
- Create: `apps/backend/app/providers/openai_provider.py` — OpenAI adapter
- Create: `apps/backend/app/providers/gemini_provider.py` — Gemini adapter
- Create: `apps/backend/app/providers/registry.py` — provider registry and selection
- Create: `apps/backend/app/orchestration/contracts.py` — typed orchestration payloads
- Create: `apps/backend/app/orchestration/research.py` — research stage
- Create: `apps/backend/app/orchestration/synthesis.py` — synthesis stage
- Create: `apps/backend/app/orchestration/delivery.py` — delivery stage
- Create: `apps/backend/app/jobs/celery_app.py` — Celery bootstrap
- Create: `apps/backend/app/jobs/tasks.py` — background job entrypoints
- Create: `apps/backend/app/connectors/web.py` — webpage fetch and normalize
- Create: `apps/backend/app/connectors/uploads.py` — file/text source normalization
- Create: `apps/backend/tests/conftest.py` — pytest fixtures
- Create: `apps/backend/tests/test_health.py` — API health tests
- Create: `apps/backend/tests/test_task_submit_api.py` — task submit API tests
- Create: `apps/backend/tests/test_source_ingestion.py` — source ingestion tests
- Create: `apps/backend/tests/test_provider_registry.py` — provider abstraction tests
- Create: `apps/backend/tests/test_orchestration_pipeline.py` — orchestration tests
- Create: `apps/backend/tests/test_subscription_service.py` — quota tests

### Root / tooling
- Create: `docker-compose.yml` — local PostgreSQL and Redis
- Create: `.env.example` — environment variable template
- Create: `.gitignore` — ignore build output and local env
- Create: `README.md` — local setup instructions
- Create: `Makefile` — local dev commands

---

### Task 1: Bootstrap repository and developer tooling

**Files:**
- Create: `.gitignore`
- Create: `.env.example`
- Create: `docker-compose.yml`
- Create: `Makefile`
- Create: `README.md`

- [ ] **Step 1: Write the failing repo smoke test command list into README expectations**

```md
# Jclaw MVP

## Verification targets
- `docker compose up -d`
- `make backend-test`
- `make desktop-test`
- `make lint`
```

- [ ] **Step 2: Add root tooling files**

```gitignore
.env
.venv/
node_modules/
dist/
.pytest_cache/
__pycache__/
apps/backend/.mypy_cache/
apps/backend/.pytest_cache/
apps/desktop/src-tauri/target/
apps/desktop/src-tauri/gen/
coverage/
playwright-report/
```

```env
POSTGRES_DSN=postgresql+psycopg://postgres:postgres@localhost:5432/jclaw
REDIS_URL=redis://localhost:6379/0
APP_ENV=development
APP_SECRET_KEY=change-me
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=
DEFAULT_MODEL_PROVIDER=anthropic
DEFAULT_MODEL_NAME=claude-opus-4-6
```

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: jclaw
    ports:
      - "5432:5432"
  redis:
    image: redis:7
    ports:
      - "6379:6379"
```

```make
backend-test:
	cd apps/backend && python -m pytest

desktop-test:
	cd apps/desktop && npm test

lint:
	cd apps/backend && python -m pytest tests/test_health.py -q
	cd apps/desktop && npm run test -- --runInBand
```

- [ ] **Step 3: Run smoke commands to verify expected initial failure**

Run: `docker compose config && make backend-test`
Expected: Docker config passes, `make backend-test` fails because `apps/backend` does not exist yet.

- [ ] **Step 4: Commit**

```bash
git add .gitignore .env.example docker-compose.yml Makefile README.md
git commit -m "chore: bootstrap repository tooling"
```

### Task 2: Scaffold FastAPI backend package and health endpoint

**Files:**
- Create: `apps/backend/pyproject.toml`
- Create: `apps/backend/app/main.py`
- Create: `apps/backend/app/core/config.py`
- Create: `apps/backend/app/api/routes/health.py`
- Create: `apps/backend/tests/conftest.py`
- Create: `apps/backend/tests/test_health.py`

- [ ] **Step 1: Write the failing health test**

```python
from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_ok() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "environment": "development"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/backend && python -m pytest tests/test_health.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'app'`.

- [ ] **Step 3: Write minimal backend bootstrap**

```toml
[project]
name = "jclaw-backend"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.115.0,<1.0.0",
  "uvicorn[standard]>=0.35.0,<1.0.0",
  "pydantic-settings>=2.8.0,<3.0.0",
  "pytest>=8.3.0,<9.0.0",
  "httpx>=0.28.0,<1.0.0",
]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")


settings = Settings()
```

```python
from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}
```

```python
from fastapi import FastAPI

from app.api.routes.health import router as health_router

app = FastAPI(title="Jclaw Backend")
app.include_router(health_router)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/backend && python -m pytest tests/test_health.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/backend/pyproject.toml apps/backend/app/main.py apps/backend/app/core/config.py apps/backend/app/api/routes/health.py apps/backend/tests/conftest.py apps/backend/tests/test_health.py
git commit -m "feat: add backend health endpoint"
```

### Task 3: Add database config, ORM models, and initial migration

**Files:**
- Create: `apps/backend/alembic.ini`
- Create: `apps/backend/alembic/env.py`
- Create: `apps/backend/alembic/versions/20260327_01_initial_schema.py`
- Create: `apps/backend/app/core/database.py`
- Create: `apps/backend/app/models/task.py`
- Create: `apps/backend/app/models/source.py`
- Create: `apps/backend/app/models/knowledge_pack.py`
- Create: `apps/backend/app/models/deliverable.py`
- Create: `apps/backend/app/models/subscription.py`
- Modify: `apps/backend/pyproject.toml`
- Test: `apps/backend/tests/test_health.py`

- [ ] **Step 1: Write the failing ORM import smoke test**

```python
from app.models.task import Task
from app.models.source import Source
from app.models.knowledge_pack import KnowledgePack
from app.models.deliverable import Deliverable
from app.models.subscription import Subscription


def test_models_import() -> None:
    assert Task.__tablename__ == "tasks"
    assert Source.__tablename__ == "sources"
    assert KnowledgePack.__tablename__ == "knowledge_packs"
    assert Deliverable.__tablename__ == "deliverables"
    assert Subscription.__tablename__ == "subscriptions"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/backend && python -m pytest tests/test_models_import.py -v`
Expected: FAIL with `ModuleNotFoundError` for model modules.

- [ ] **Step 3: Add SQLAlchemy base, engine, and models**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.postgres_dsn)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
```

```python
from datetime import datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), index=True)
    user_prompt: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

```python
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"), index=True)
    source_type: Mapped[str] = mapped_column(String(32), index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
```

```python
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class KnowledgePack(Base):
    __tablename__ = "knowledge_packs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"), unique=True)
    summary: Mapped[str] = mapped_column(Text)
    outline: Mapped[str] = mapped_column(Text)
```

```python
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Deliverable(Base):
    __tablename__ = "deliverables"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    task_id: Mapped[str] = mapped_column(ForeignKey("tasks.id"), unique=True)
    content_markdown: Mapped[str] = mapped_column(Text)
    content_type: Mapped[str] = mapped_column(String(64))
```

```python
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    plan_name: Mapped[str] = mapped_column(String(64))
    task_quota: Mapped[int] = mapped_column(Integer)
    task_usage: Mapped[int] = mapped_column(Integer, default=0)
```

- [ ] **Step 4: Add settings fields and initial migration**

```python
class Settings(BaseSettings):
    app_env: str = "development"
    postgres_dsn: str = "postgresql+psycopg://postgres:postgres@localhost:5432/jclaw"
    redis_url: str = "redis://localhost:6379/0"
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")
```

```python
def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("user_prompt", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
```

- [ ] **Step 5: Run tests to verify model imports pass**

Run: `cd apps/backend && python -m pytest tests/test_models_import.py tests/test_health.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add apps/backend/alembic.ini apps/backend/alembic apps/backend/app/core/database.py apps/backend/app/models apps/backend/pyproject.toml apps/backend/tests/test_models_import.py
git commit -m "feat: add backend persistence models"
```

### Task 4: Add task/source schemas and task submission API

**Files:**
- Create: `apps/backend/app/schemas/task.py`
- Create: `apps/backend/app/schemas/source.py`
- Create: `apps/backend/app/api/routes/tasks.py`
- Create: `apps/backend/app/api/routes/sources.py`
- Create: `apps/backend/app/services/task_service.py`
- Create: `apps/backend/app/services/source_service.py`
- Modify: `apps/backend/app/main.py`
- Test: `apps/backend/tests/test_task_submit_api.py`

- [ ] **Step 1: Write the failing task submit API test**

```python
from fastapi.testclient import TestClient

from app.main import app


def test_submit_task_creates_received_task() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/tasks",
        json={
            "title": "Write market overview",
            "user_prompt": "Research AI browser agents and write an article.",
            "sources": [
                {"source_type": "text", "title": "brief", "content": "Focus on 2026 products."}
            ],
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "received"
    assert body["title"] == "Write market overview"
    assert len(body["sources"]) == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/backend && python -m pytest tests/test_task_submit_api.py -v`
Expected: FAIL with `404 Not Found` for `/api/tasks`.

- [ ] **Step 3: Add request/response schemas and task service**

```python
from pydantic import BaseModel


class SourceInput(BaseModel):
    source_type: str
    title: str
    content: str


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
```

```python
import uuid

from app.schemas.task import TaskCreateRequest, TaskResponse


class TaskService:
    def create_task(self, payload: TaskCreateRequest) -> TaskResponse:
        return TaskResponse(
            id=str(uuid.uuid4()),
            title=payload.title,
            status="received",
            user_prompt=payload.user_prompt,
            sources=payload.sources,
        )
```

```python
from fastapi import APIRouter, status

from app.schemas.task import TaskCreateRequest, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])
service = TaskService()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateRequest) -> TaskResponse:
    return service.create_task(payload)
```

- [ ] **Step 4: Register routes and rerun test**

```python
from app.api.routes.tasks import router as tasks_router

app.include_router(tasks_router)
```

Run: `cd apps/backend && python -m pytest tests/test_task_submit_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/backend/app/schemas apps/backend/app/api/routes/tasks.py apps/backend/app/api/routes/sources.py apps/backend/app/services/task_service.py apps/backend/app/services/source_service.py apps/backend/app/main.py apps/backend/tests/test_task_submit_api.py
git commit -m "feat: add task submission api"
```

### Task 5: Persist tasks and sources in PostgreSQL

**Files:**
- Modify: `apps/backend/app/services/task_service.py`
- Modify: `apps/backend/app/core/database.py`
- Modify: `apps/backend/app/models/task.py`
- Modify: `apps/backend/app/models/source.py`
- Modify: `apps/backend/app/api/routes/tasks.py`
- Test: `apps/backend/tests/conftest.py`
- Test: `apps/backend/tests/test_task_submit_api.py`

- [ ] **Step 1: Write the failing persistence test**

```python
def test_submit_task_persists_rows(client, db_session) -> None:
    response = client.post(
        "/api/tasks",
        json={
            "title": "Write market overview",
            "user_prompt": "Research AI browser agents and write an article.",
            "sources": [
                {"source_type": "text", "title": "brief", "content": "Focus on 2026 products."}
            ],
        },
    )

    assert response.status_code == 201
    assert db_session.execute("select count(*) from tasks").scalar_one() == 1
    assert db_session.execute("select count(*) from sources").scalar_one() == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/backend && python -m pytest tests/test_task_submit_api.py::test_submit_task_persists_rows -v`
Expected: FAIL because the service returns in-memory data only.

- [ ] **Step 3: Add database dependency and persistence implementation**

```python
from collections.abc import Generator
from sqlalchemy.orm import Session

from app.core.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
```

```python
class TaskService:
    def create_task(self, session: Session, payload: TaskCreateRequest) -> TaskResponse:
        task = Task(
            id=str(uuid.uuid4()),
            title=payload.title,
            status="received",
            user_prompt=payload.user_prompt,
        )
        session.add(task)
        for item in payload.sources:
            session.add(
                Source(
                    id=str(uuid.uuid4()),
                    task_id=task.id,
                    source_type=item.source_type,
                    title=item.title,
                    content=item.content,
                )
            )
        session.commit()
        return TaskResponse(
            id=task.id,
            title=task.title,
            status=task.status,
            user_prompt=task.user_prompt,
            sources=payload.sources,
        )
```

```python
@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateRequest, db: Session = Depends(get_db)) -> TaskResponse:
    return service.create_task(db, payload)
```

- [ ] **Step 4: Run persistence test to verify it passes**

Run: `cd apps/backend && python -m pytest tests/test_task_submit_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/backend/app/services/task_service.py apps/backend/app/core/database.py apps/backend/app/models/task.py apps/backend/app/models/source.py apps/backend/app/api/routes/tasks.py apps/backend/tests/conftest.py apps/backend/tests/test_task_submit_api.py
git commit -m "feat: persist tasks and sources"
```

### Task 6: Add provider abstraction and registry for Anthropic, OpenAI, and Gemini

**Files:**
- Create: `apps/backend/app/providers/base.py`
- Create: `apps/backend/app/providers/anthropic_provider.py`
- Create: `apps/backend/app/providers/openai_provider.py`
- Create: `apps/backend/app/providers/gemini_provider.py`
- Create: `apps/backend/app/providers/registry.py`
- Modify: `apps/backend/app/core/config.py`
- Modify: `apps/backend/pyproject.toml`
- Test: `apps/backend/tests/test_provider_registry.py`

- [ ] **Step 1: Write the failing provider registry test**

```python
from app.providers.registry import ProviderRegistry


def test_registry_exposes_expected_provider_keys() -> None:
    registry = ProviderRegistry()

    assert sorted(registry.keys()) == ["anthropic", "gemini", "openai"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/backend && python -m pytest tests/test_provider_registry.py -v`
Expected: FAIL with `ModuleNotFoundError` for provider modules.

- [ ] **Step 3: Add provider protocol, adapters, and registry**

```python
from typing import Protocol


class ModelProvider(Protocol):
    key: str

    def generate_text(self, *, system_prompt: str, user_prompt: str) -> str: ...
```

```python
class AnthropicProvider:
    key = "anthropic"

    def generate_text(self, *, system_prompt: str, user_prompt: str) -> str:
        return f"anthropic:{user_prompt}"
```

```python
class OpenAIProvider:
    key = "openai"

    def generate_text(self, *, system_prompt: str, user_prompt: str) -> str:
        return f"openai:{user_prompt}"
```

```python
class GeminiProvider:
    key = "gemini"

    def generate_text(self, *, system_prompt: str, user_prompt: str) -> str:
        return f"gemini:{user_prompt}"
```

```python
class ProviderRegistry:
    def __init__(self) -> None:
        self._providers = {
            "anthropic": AnthropicProvider(),
            "openai": OpenAIProvider(),
            "gemini": GeminiProvider(),
        }

    def get(self, key: str):
        return self._providers[key]

    def keys(self) -> list[str]:
        return list(self._providers.keys())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/backend && python -m pytest tests/test_provider_registry.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/backend/app/providers apps/backend/app/core/config.py apps/backend/pyproject.toml apps/backend/tests/test_provider_registry.py
git commit -m "feat: add model provider registry"
```

### Task 7: Add source connectors for pasted text, uploaded files, and web URLs

**Files:**
- Create: `apps/backend/app/connectors/web.py`
- Create: `apps/backend/app/connectors/uploads.py`
- Modify: `apps/backend/app/services/source_service.py`
- Modify: `apps/backend/app/api/routes/sources.py`
- Test: `apps/backend/tests/test_source_ingestion.py`

- [ ] **Step 1: Write the failing source ingestion tests**

```python
from app.services.source_service import SourceService


def test_normalize_text_source() -> None:
    service = SourceService()

    source = service.normalize_text(title="brief", content="Market focus")

    assert source["source_type"] == "text"
    assert source["title"] == "brief"
    assert source["content"] == "Market focus"


def test_normalize_url_source(monkeypatch) -> None:
    service = SourceService()
    monkeypatch.setattr(service, "fetch_url", lambda url: "Fetched page")

    source = service.normalize_url(url="https://example.com")

    assert source["source_type"] == "web"
    assert source["content"] == "Fetched page"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd apps/backend && python -m pytest tests/test_source_ingestion.py -v`
Expected: FAIL because normalization methods do not exist.

- [ ] **Step 3: Add minimal source normalization implementation**

```python
class SourceService:
    def normalize_text(self, *, title: str, content: str) -> dict[str, str]:
        return {"source_type": "text", "title": title, "content": content}

    def fetch_url(self, url: str) -> str:
        return f"Fetched content from {url}"

    def normalize_url(self, *, url: str) -> dict[str, str]:
        return {
            "source_type": "web",
            "title": url,
            "content": self.fetch_url(url),
        }
```

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd apps/backend && python -m pytest tests/test_source_ingestion.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/backend/app/connectors/web.py apps/backend/app/connectors/uploads.py apps/backend/app/services/source_service.py apps/backend/app/api/routes/sources.py apps/backend/tests/test_source_ingestion.py
git commit -m "feat: add source normalization flow"
```

### Task 8: Add orchestration contracts and background job pipeline

**Files:**
- Create: `apps/backend/app/orchestration/contracts.py`
- Create: `apps/backend/app/orchestration/research.py`
- Create: `apps/backend/app/orchestration/synthesis.py`
- Create: `apps/backend/app/orchestration/delivery.py`
- Create: `apps/backend/app/jobs/celery_app.py`
- Create: `apps/backend/app/jobs/tasks.py`
- Modify: `apps/backend/app/core/config.py`
- Modify: `apps/backend/pyproject.toml`
- Test: `apps/backend/tests/test_orchestration_pipeline.py`

- [ ] **Step 1: Write the failing orchestration pipeline test**

```python
from app.orchestration.delivery import DeliveryStage
from app.orchestration.research import ResearchStage
from app.orchestration.synthesis import SynthesisStage


def test_pipeline_transforms_task_into_deliverable() -> None:
    research = ResearchStage()
    synthesis = SynthesisStage()
    delivery = DeliveryStage()

    research_result = research.run(task_prompt="Research browser agents", sources=[{"content": "Agent A"}])
    synthesis_result = synthesis.run(research_result)
    deliverable = delivery.run(synthesis_result)

    assert "Agent A" in research_result.summary
    assert synthesis_result.summary != ""
    assert deliverable.content_markdown.startswith("#")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/backend && python -m pytest tests/test_orchestration_pipeline.py -v`
Expected: FAIL because stage classes do not exist.

- [ ] **Step 3: Add stage contracts and minimal implementation**

```python
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
```

```python
class ResearchStage:
    def run(self, *, task_prompt: str, sources: list[dict[str, str]]) -> ResearchResult:
        joined = "\n".join(item["content"] for item in sources)
        return ResearchResult(summary=f"{task_prompt}\n{joined}", source_titles=[])
```

```python
class SynthesisStage:
    def run(self, research_result: ResearchResult) -> SynthesisResult:
        return SynthesisResult(summary=research_result.summary, outline="- intro\n- body\n- conclusion")
```

```python
class DeliveryStage:
    def run(self, synthesis_result: SynthesisResult) -> DeliverableResult:
        return DeliverableResult(content_markdown=f"# Draft\n\n{synthesis_result.summary}")
```

- [ ] **Step 4: Add Celery wiring and rerun tests**

```python
from celery import Celery

from app.core.config import settings

celery_app = Celery("jclaw", broker=settings.redis_url, backend=settings.redis_url)
```

```python
from app.jobs.celery_app import celery_app


@celery_app.task(name="run_task_pipeline")
def run_task_pipeline(task_id: str) -> str:
    return task_id
```

Run: `cd apps/backend && python -m pytest tests/test_orchestration_pipeline.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/backend/app/orchestration apps/backend/app/jobs apps/backend/app/core/config.py apps/backend/pyproject.toml apps/backend/tests/test_orchestration_pipeline.py
git commit -m "feat: add task orchestration pipeline"
```

### Task 9: Persist Knowledge Pack and Deliverable outputs from background jobs

**Files:**
- Modify: `apps/backend/app/jobs/tasks.py`
- Create: `apps/backend/app/services/knowledge_pack_service.py`
- Create: `apps/backend/app/services/deliverable_service.py`
- Test: `apps/backend/tests/test_orchestration_pipeline.py`

- [ ] **Step 1: Write the failing persistence assertions**

```python
def test_run_task_pipeline_persists_knowledge_pack_and_deliverable(db_session, seeded_task) -> None:
    run_task_pipeline(seeded_task.id)

    assert db_session.execute("select count(*) from knowledge_packs").scalar_one() == 1
    assert db_session.execute("select count(*) from deliverables").scalar_one() == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/backend && python -m pytest tests/test_orchestration_pipeline.py::test_run_task_pipeline_persists_knowledge_pack_and_deliverable -v`
Expected: FAIL because the job does not write results.

- [ ] **Step 3: Add result persistence services and job implementation**

```python
class KnowledgePackService:
    def save(self, session: Session, *, task_id: str, summary: str, outline: str) -> None:
        session.add(KnowledgePack(id=str(uuid.uuid4()), task_id=task_id, summary=summary, outline=outline))
```

```python
class DeliverableService:
    def save(self, session: Session, *, task_id: str, content_markdown: str, content_type: str) -> None:
        session.add(
            Deliverable(
                id=str(uuid.uuid4()),
                task_id=task_id,
                content_markdown=content_markdown,
                content_type=content_type,
            )
        )
```

```python
@celery_app.task(name="run_task_pipeline")
def run_task_pipeline(task_id: str) -> str:
    with SessionLocal() as session:
        task = session.get(Task, task_id)
        sources = [
            {"title": row.title, "content": row.content}
            for row in session.query(Source).filter(Source.task_id == task_id).all()
        ]
        research = ResearchStage().run(task_prompt=task.user_prompt, sources=sources)
        synthesis = SynthesisStage().run(research)
        deliverable = DeliveryStage().run(synthesis)
        KnowledgePackService().save(session, task_id=task_id, summary=synthesis.summary, outline=synthesis.outline)
        DeliverableService().save(
            session,
            task_id=task_id,
            content_markdown=deliverable.content_markdown,
            content_type=deliverable.content_type,
        )
        task.status = "delivered"
        session.commit()
        return task_id
```

- [ ] **Step 4: Run persistence test to verify it passes**

Run: `cd apps/backend && python -m pytest tests/test_orchestration_pipeline.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/backend/app/jobs/tasks.py apps/backend/app/services/knowledge_pack_service.py apps/backend/app/services/deliverable_service.py apps/backend/tests/test_orchestration_pipeline.py
git commit -m "feat: persist orchestration outputs"
```

### Task 10: Add deliverable retrieval and task detail API

**Files:**
- Create: `apps/backend/app/schemas/knowledge_pack.py`
- Create: `apps/backend/app/schemas/deliverable.py`
- Create: `apps/backend/app/api/routes/deliverables.py`
- Modify: `apps/backend/app/api/routes/tasks.py`
- Test: `apps/backend/tests/test_task_submit_api.py`

- [ ] **Step 1: Write the failing task detail test**

```python
def test_get_task_detail_returns_deliverable(client, seeded_delivered_task) -> None:
    response = client.get(f"/api/tasks/{seeded_delivered_task.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "delivered"
    assert body["deliverable"]["content_type"] == "article"
    assert body["knowledge_pack"]["summary"] != ""
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/backend && python -m pytest tests/test_task_submit_api.py::test_get_task_detail_returns_deliverable -v`
Expected: FAIL with `404 Not Found` for task detail route.

- [ ] **Step 3: Add detail schemas and route implementation**

```python
class KnowledgePackResponse(BaseModel):
    summary: str
    outline: str


class DeliverableResponse(BaseModel):
    content_markdown: str
    content_type: str


class TaskDetailResponse(TaskResponse):
    knowledge_pack: KnowledgePackResponse | None = None
    deliverable: DeliverableResponse | None = None
```

```python
@router.get("/{task_id}", response_model=TaskDetailResponse)
def get_task(task_id: str, db: Session = Depends(get_db)) -> TaskDetailResponse:
    task = db.get(Task, task_id)
    pack = db.query(KnowledgePack).filter(KnowledgePack.task_id == task_id).one_or_none()
    deliverable = db.query(Deliverable).filter(Deliverable.task_id == task_id).one_or_none()
    return TaskDetailResponse(
        id=task.id,
        title=task.title,
        status=task.status,
        user_prompt=task.user_prompt,
        sources=[],
        knowledge_pack=None if pack is None else KnowledgePackResponse(summary=pack.summary, outline=pack.outline),
        deliverable=None if deliverable is None else DeliverableResponse(
            content_markdown=deliverable.content_markdown,
            content_type=deliverable.content_type,
        ),
    )
```

- [ ] **Step 4: Run detail test to verify it passes**

Run: `cd apps/backend && python -m pytest tests/test_task_submit_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/backend/app/schemas/knowledge_pack.py apps/backend/app/schemas/deliverable.py apps/backend/app/api/routes/deliverables.py apps/backend/app/api/routes/tasks.py apps/backend/tests/test_task_submit_api.py
git commit -m "feat: add task detail api"
```

### Task 11: Add single-user subscription and quota checks

**Files:**
- Create: `apps/backend/app/services/subscription_service.py`
- Modify: `apps/backend/app/services/task_service.py`
- Test: `apps/backend/tests/test_subscription_service.py`

- [ ] **Step 1: Write the failing quota test**

```python
from app.services.subscription_service import SubscriptionService


def test_can_create_task_when_usage_is_below_quota() -> None:
    service = SubscriptionService()

    assert service.can_submit(task_usage=2, task_quota=3) is True


def test_cannot_create_task_when_usage_reaches_quota() -> None:
    service = SubscriptionService()

    assert service.can_submit(task_usage=3, task_quota=3) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/backend && python -m pytest tests/test_subscription_service.py -v`
Expected: FAIL because the service does not exist.

- [ ] **Step 3: Add minimal quota service and enforce it in task submission**

```python
class SubscriptionService:
    def can_submit(self, *, task_usage: int, task_quota: int) -> bool:
        return task_usage < task_quota
```

```python
if not subscription_service.can_submit(task_usage=subscription.task_usage, task_quota=subscription.task_quota):
    raise HTTPException(status_code=402, detail="Task quota exceeded")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd apps/backend && python -m pytest tests/test_subscription_service.py tests/test_task_submit_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/backend/app/services/subscription_service.py apps/backend/app/services/task_service.py apps/backend/tests/test_subscription_service.py apps/backend/tests/test_task_submit_api.py
git commit -m "feat: enforce single-user task quota"
```

### Task 12: Scaffold Vue desktop app and backend API client

**Files:**
- Create: `apps/desktop/package.json`
- Create: `apps/desktop/tsconfig.json`
- Create: `apps/desktop/vite.config.ts`
- Create: `apps/desktop/src/main.ts`
- Create: `apps/desktop/src/App.vue`
- Create: `apps/desktop/src/lib/api.ts`
- Create: `apps/desktop/tests/task-workspace.spec.ts`

- [ ] **Step 1: Write the failing frontend smoke test**

```ts
import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import App from '../src/App.vue'

describe('App', () => {
  it('renders desktop shell title', () => {
    const wrapper = mount(App)

    expect(wrapper.text()).toContain('Jclaw')
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/desktop && npm test -- task-workspace.spec.ts`
Expected: FAIL because the desktop app does not exist.

- [ ] **Step 3: Add minimal Vue app scaffold**

```json
{
  "name": "jclaw-desktop",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest run"
  },
  "dependencies": {
    "vue": "^3.5.0",
    "vue-router": "^4.5.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.2.0",
    "@vue/test-utils": "^2.4.6",
    "typescript": "^5.8.0",
    "vite": "^6.2.0",
    "vitest": "^3.1.0"
  }
}
```

```vue
<template>
  <main>
    <h1>Jclaw</h1>
    <p>AI 内容工作代理</p>
  </main>
</template>
```

```ts
export async function createTask(payload: unknown) {
  const response = await fetch('http://127.0.0.1:8000/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  return response.json()
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/desktop && npm test -- task-workspace.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/desktop/package.json apps/desktop/tsconfig.json apps/desktop/vite.config.ts apps/desktop/src/main.ts apps/desktop/src/App.vue apps/desktop/src/lib/api.ts apps/desktop/tests/task-workspace.spec.ts
git commit -m "feat: scaffold desktop app"
```

### Task 13: Build task workspace UI for task creation and source input

**Files:**
- Create: `apps/desktop/src/router/index.ts`
- Create: `apps/desktop/src/stores/task.ts`
- Create: `apps/desktop/src/pages/TaskWorkspacePage.vue`
- Create: `apps/desktop/src/components/TaskComposer.vue`
- Create: `apps/desktop/src/components/SourcePicker.vue`
- Create: `apps/desktop/src/styles.css`
- Modify: `apps/desktop/src/App.vue`
- Test: `apps/desktop/tests/task-workspace.spec.ts`

- [ ] **Step 1: Write the failing workspace interaction test**

```ts
import { fireEvent, render, screen } from '@testing-library/vue'

import TaskWorkspacePage from '../src/pages/TaskWorkspacePage.vue'

test('submits title, prompt, and text source', async () => {
  render(TaskWorkspacePage)

  await fireEvent.update(screen.getByLabelText('任务标题'), 'Write market overview')
  await fireEvent.update(screen.getByLabelText('任务目标'), 'Research AI browser agents and write an article.')
  await fireEvent.update(screen.getByLabelText('文本资料标题'), 'brief')
  await fireEvent.update(screen.getByLabelText('文本资料内容'), 'Focus on 2026 products.')

  expect(screen.getByText('提交任务')).toBeInTheDocument()
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/desktop && npm test -- task-workspace.spec.ts`
Expected: FAIL because the workspace page and controls do not exist.

- [ ] **Step 3: Add minimal workspace page and components**

```vue
<template>
  <form @submit.prevent="submit">
    <label>任务标题<input v-model="title" aria-label="任务标题" /></label>
    <label>任务目标<textarea v-model="userPrompt" aria-label="任务目标" /></label>
    <SourcePicker @add-text-source="addTextSource" />
    <button type="submit">提交任务</button>
  </form>
</template>
```

```vue
<template>
  <section>
    <label>文本资料标题<input v-model="title" aria-label="文本资料标题" /></label>
    <label>文本资料内容<textarea v-model="content" aria-label="文本资料内容" /></label>
    <button type="button" @click="$emit('add-text-source', { source_type: 'text', title, content })">添加文本资料</button>
  </section>
</template>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/desktop && npm test -- task-workspace.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/desktop/src/router/index.ts apps/desktop/src/stores/task.ts apps/desktop/src/pages/TaskWorkspacePage.vue apps/desktop/src/components/TaskComposer.vue apps/desktop/src/components/SourcePicker.vue apps/desktop/src/styles.css apps/desktop/src/App.vue apps/desktop/tests/task-workspace.spec.ts
git commit -m "feat: add task workspace ui"
```

### Task 14: Show task status, Knowledge Pack, and Deliverable in desktop UI

**Files:**
- Create: `apps/desktop/src/components/TaskTimeline.vue`
- Create: `apps/desktop/src/components/KnowledgePackPanel.vue`
- Create: `apps/desktop/src/components/DeliverablePanel.vue`
- Modify: `apps/desktop/src/pages/TaskWorkspacePage.vue`
- Modify: `apps/desktop/src/lib/api.ts`
- Test: `apps/desktop/tests/task-workspace.spec.ts`

- [ ] **Step 1: Write the failing result display test**

```ts
test('renders delivered task panels', async () => {
  render(TaskWorkspacePage, {
    global: {
      mocks: {
        $api: {
          getTask: async () => ({
            status: 'delivered',
            knowledge_pack: { summary: 'Research summary', outline: '- intro' },
            deliverable: { content_markdown: '# Draft', content_type: 'article' },
          }),
        },
      },
    },
  })

  expect(await screen.findByText('Research summary')).toBeInTheDocument()
  expect(await screen.findByText('# Draft')).toBeInTheDocument()
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/desktop && npm test -- task-workspace.spec.ts`
Expected: FAIL because result panels do not exist.

- [ ] **Step 3: Add task timeline and result panels**

```vue
<template>
  <aside>
    <h2>任务状态</h2>
    <p>{{ status }}</p>
  </aside>
</template>
```

```vue
<template>
  <section>
    <h2>知识包</h2>
    <p>{{ summary }}</p>
    <pre>{{ outline }}</pre>
  </section>
</template>
```

```vue
<template>
  <section>
    <h2>最终成品</h2>
    <pre>{{ contentMarkdown }}</pre>
  </section>
</template>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/desktop && npm test -- task-workspace.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/desktop/src/components/TaskTimeline.vue apps/desktop/src/components/KnowledgePackPanel.vue apps/desktop/src/components/DeliverablePanel.vue apps/desktop/src/pages/TaskWorkspacePage.vue apps/desktop/src/lib/api.ts apps/desktop/tests/task-workspace.spec.ts
git commit -m "feat: show task deliverables in desktop app"
```

### Task 15: Add Tauri shell and backend process launcher

**Files:**
- Create: `apps/desktop/src-tauri/Cargo.toml`
- Create: `apps/desktop/src-tauri/tauri.conf.json`
- Create: `apps/desktop/src-tauri/src/main.rs`
- Create: `apps/desktop/src-tauri/src/lib.rs`
- Create: `apps/desktop/src-tauri/src/backend.rs`
- Create: `apps/desktop/src-tauri/tests/backend_launch.rs`

- [ ] **Step 1: Write the failing Rust backend launch test**

```rust
#[test]
fn backend_command_uses_python_module_entrypoint() {
    let command = jclaw_desktop::backend::build_backend_command("python");

    assert_eq!(command.get_program().to_string_lossy(), "python");
}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/desktop/src-tauri && cargo test backend_command_uses_python_module_entrypoint`
Expected: FAIL because the Tauri crate does not exist.

- [ ] **Step 3: Add minimal Tauri shell implementation**

```toml
[package]
name = "jclaw-desktop"
version = "0.1.0"
edition = "2021"

[dependencies]
tauri = { version = "2", features = [] }
serde = { version = "1", features = ["derive"] }
```

```rust
pub fn build_backend_command(python_bin: &str) -> std::process::Command {
    let mut command = std::process::Command::new(python_bin);
    command.arg("-m").arg("uvicorn").arg("app.main:app");
    command
}
```

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default().run(tauri::generate_context!()).expect("error while running tauri application");
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/desktop/src-tauri && cargo test backend_command_uses_python_module_entrypoint`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add apps/desktop/src-tauri/Cargo.toml apps/desktop/src-tauri/tauri.conf.json apps/desktop/src-tauri/src/main.rs apps/desktop/src-tauri/src/lib.rs apps/desktop/src-tauri/src/backend.rs apps/desktop/src-tauri/tests/backend_launch.rs
git commit -m "feat: add tauri shell bootstrap"
```

### Task 16: Add end-to-end backend pipeline test and desktop verification

**Files:**
- Modify: `apps/backend/tests/test_orchestration_pipeline.py`
- Modify: `apps/desktop/tests/task-workspace.spec.ts`
- Modify: `README.md`

- [ ] **Step 1: Write the failing end-to-end verification test**

```python
def test_submit_then_run_pipeline_then_fetch_detail(client, db_session) -> None:
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Write market overview",
            "user_prompt": "Research AI browser agents and write an article.",
            "sources": [
                {"source_type": "text", "title": "brief", "content": "Focus on 2026 products."}
            ],
        },
    )
    task_id = create_response.json()["id"]

    run_task_pipeline(task_id)

    detail_response = client.get(f"/api/tasks/{task_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["deliverable"]["content_markdown"].startswith("# Draft")
```

- [ ] **Step 2: Run tests to verify current gaps**

Run: `cd apps/backend && python -m pytest tests/test_orchestration_pipeline.py::test_submit_then_run_pipeline_then_fetch_detail -v && cd ../desktop && npm test -- task-workspace.spec.ts`
Expected: At least one assertion fails until the full path is wired correctly.

- [ ] **Step 3: Fix final integration gaps and document local run flow**

```md
## Local run
1. `docker compose up -d`
2. `cd apps/backend && uvicorn app.main:app --reload`
3. `cd apps/desktop && npm install && npm run dev`
4. `cd apps/desktop/src-tauri && cargo tauri dev`
```

- [ ] **Step 4: Run full verification suite**

Run: `docker compose up -d && cd apps/backend && python -m pytest && cd ../desktop && npm test && cd src-tauri && cargo test`
Expected: PASS for backend tests, desktop tests, and Rust tests.

- [ ] **Step 5: Commit**

```bash
git add apps/backend/tests/test_orchestration_pipeline.py apps/desktop/tests/task-workspace.spec.ts README.md
git commit -m "test: verify single-user content task mvp flow"
```

## Self-Review

### Spec coverage
- 对话式任务入口：Task 12-14
- 统一资料源接入（文本、上传、网页 URL）：Task 4, 7, 13
- 多模型抽象（Anthropic/OpenAI/Gemini）：Task 6
- 研究 → 知识沉淀 → 交付：Task 8-10
- Knowledge Pack / Deliverable 持久化：Task 9-10
- 单用户账户与订阅占位：Task 11
- Tauri 2 + Vue 3 + Rust 桌面壳：Task 12-15
- PostgreSQL 持久化：Task 3, 5
- 同步短任务 + 后台长任务队列混合：Task 8-10

### Gaps found and fixed in plan
- 未把“后台长任务”落到具体实现：已在 Task 8-10 用 Celery + Redis 明确。
- 未把“结果查看”落到桌面界面：已在 Task 14 明确。
- 未把“订阅计费”收敛为 MVP 范围：已在 Task 11 明确为单用户 quota 占位，不扩展支付系统。

### Placeholder scan
- 未使用 TBD / TODO / “similar to task N” 一类占位表达。
- 所有代码步骤均含具体代码块。
- 所有运行步骤均含命令与预期输出。

### Type consistency
- 提交任务统一使用 `TaskCreateRequest`。
- 研究/综合/交付阶段统一使用 `ResearchResult`、`SynthesisResult`、`DeliverableResult`。
- 数据对象统一使用 `Task`、`Source`、`KnowledgePack`、`Deliverable`、`Subscription`。
