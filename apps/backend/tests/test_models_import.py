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
