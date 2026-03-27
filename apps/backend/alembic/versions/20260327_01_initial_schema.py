"""initial schema

Revision ID: 20260327_01
Revises:
Create Date: 2026-03-27
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260327_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("user_prompt", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("plan_name", sa.String(length=64), nullable=False),
        sa.Column("task_quota", sa.Integer(), nullable=False),
        sa.Column("task_usage", sa.Integer(), nullable=False),
    )

    op.create_table(
        "sources",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("task_id", sa.String(length=36), sa.ForeignKey("tasks.id"), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
    )
    op.create_index("ix_sources_task_id", "sources", ["task_id"])
    op.create_index("ix_sources_source_type", "sources", ["source_type"])

    op.create_table(
        "knowledge_packs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("task_id", sa.String(length=36), sa.ForeignKey("tasks.id"), nullable=False, unique=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("outline", sa.Text(), nullable=False),
    )

    op.create_table(
        "deliverables",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("task_id", sa.String(length=36), sa.ForeignKey("tasks.id"), nullable=False, unique=True),
        sa.Column("content_markdown", sa.Text(), nullable=False),
        sa.Column("content_type", sa.String(length=64), nullable=False),
    )

    op.create_index("ix_tasks_status", "tasks", ["status"])


def downgrade() -> None:
    op.drop_index("ix_tasks_status", table_name="tasks")
    op.drop_table("deliverables")
    op.drop_table("knowledge_packs")
    op.drop_index("ix_sources_source_type", table_name="sources")
    op.drop_index("ix_sources_task_id", table_name="sources")
    op.drop_table("sources")
    op.drop_table("subscriptions")
    op.drop_table("tasks")
