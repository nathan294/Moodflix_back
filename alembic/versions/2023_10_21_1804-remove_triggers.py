"""remove_triggers

Revision ID: fe4331f34d54
Revises: 98a6f6ebe08f
Create Date: 2023-10-21 18:04:38.996917

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fe4331f34d54"
down_revision: Union[str, None] = "98a6f6ebe08f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    DROP TRIGGER IF EXISTS create_notes_list_for_new_user ON "user";
    """
    )

    op.execute(
        """
    DROP FUNCTION IF EXISTS create_notes_list_for_new_user();
    """
    )
    op.execute(
        """
    DROP TRIGGER IF EXISTS trigger_create_movie_list_for_new_user ON "user";
    """
    )

    op.execute(
        """
    DROP FUNCTION IF EXISTS create_movie_list_for_new_user();
    """
    )
    pass


def downgrade() -> None:
    op.execute(
        """
    CREATE OR REPLACE FUNCTION create_movie_list_for_new_user()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO movie_list (id, user_id, title, status, locked, created_at, updated_at)
        VALUES (uuid_generate_v4(), NEW.firebase_id, 'Envies', 'activated', true, NOW(), NOW());
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
    )

    op.execute(
        """
    CREATE TRIGGER trigger_create_movie_list_for_new_user
    AFTER INSERT ON "user"
    FOR EACH ROW EXECUTE FUNCTION create_movie_list_for_new_user();

    """
    )
    op.execute(
        """
    CREATE OR REPLACE FUNCTION create_notes_list_for_new_user()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO movie_list (id, user_id, title, status, locked, created_at, updated_at)
        VALUES (uuid_generate_v4(), NEW.firebase_id, 'Notes', 'activated', true, NOW(), NOW());
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
    )

    op.execute(
        """
    CREATE TRIGGER create_notes_list_for_new_user
    AFTER INSERT ON "user"
    FOR EACH ROW EXECUTE FUNCTION create_notes_list_for_new_user();

    """
    )
    pass
