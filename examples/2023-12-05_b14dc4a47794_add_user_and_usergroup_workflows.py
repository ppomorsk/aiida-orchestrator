"""add User and UserGroup workflows.

Revision ID: b14dc4a47794
Revises: 8779c7b3b73e
Create Date: 2023-12-05 06:09:00.937229
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b14dc4a47794'
down_revision = '8779c7b3b73e'
branch_labels = None
depends_on = None


from orchestrator.migrations.helpers import create_workflow, delete_workflow

new_workflows = [
    {
        "name": "create_user_group",
        "target": "CREATE",
        "description": "Create user group",
        "product_type": "UserGroup"
    },
    {
        "name": "modify_user_group",
        "target": "MODIFY",
        "description": "Modify user group",
        "product_type": "UserGroup"
    },
    {
        "name": "terminate_user_group",
        "target": "TERMINATE",
        "description": "Terminate user group",
        "product_type": "UserGroup"
    },
    {
        "name": "create_user",
        "target": "CREATE",
        "description": "Create user",
        "product_type": "User"
    },
    {
        "name": "modify_user",
        "target": "MODIFY",
        "description": "Modify user",
        "product_type": "User"
    },
    {
        "name": "terminate_user",
        "target": "TERMINATE",
        "description": "Terminate user",
        "product_type": "User"
    }
]

params = dict(
    name="task_sync_from",
    target="SYSTEM",
    description="Nightly get cluster load data",
)


def upgrade() -> None:
    conn = op.get_bind()
    for workflow in new_workflows:
        create_workflow(conn, workflow)
    conn.execute(
        sa.text(
            """
            INSERT INTO workflows(name, target, description)
                VALUES (:name, :target, :description)
            """
        ),
        params,
    )

def downgrade() -> None:
    conn = op.get_bind()
    for workflow in new_workflows:
        delete_workflow(conn, workflow["name"])
