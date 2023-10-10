"""movie_list

Revision ID: 1f23cd948ee2
Revises: a8d4725123bd
Create Date: 2023-10-10 09:49:25.312433

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1f23cd948ee2"
down_revision: Union[str, None] = "a8d4725123bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "movie_list",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("status", sa.Enum("activated", "archived", "deleted", name="statusenum"), nullable=False),
        sa.Column("locked", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.firebase_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create the uuid-ossp extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    # SQL for creating the trigger
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
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("movie_list")

    # SQL for dropping the trigger
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

    # Drop the custom enum type
    op.execute(
        """
    DROP TYPE IF EXISTS statusenum;
    """
    )

    # Optionally, drop the uuid-ossp extension
    # Comment this out if other parts of your database are using it
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')

    # ### end Alembic commands ###