"""email unico y en minusculas, columnas mas amplias

Revision ID: 14d7ab10fa87
Revises: e3976be6c749
Create Date: 2026-11-05 19:13:50.243201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '14d7ab10fa87'
down_revision: Union[str, Sequence[str], None] = 'e3976be6c749'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Normaliza los correos que ya existen.
    #    Va primero: si quedara despues de la restriccion unica y dos correos
    #    chocaran al bajarlos, la migracion reventaria a mitad de camino.
    op.execute("UPDATE users SET email = lower(trim(email))")

    # 2. Columnas mas amplias
    op.alter_column('tasks', 'title',
        existing_type=sa.VARCHAR(length=30),
        type_=sa.String(length=100),
        existing_nullable=False)

    op.alter_column('users', 'email',
        existing_type=sa.VARCHAR(length=40),
        type_=sa.String(length=254),
        existing_nullable=False)

    # 3. El correo no se repite. Con nombre explicito para poder quitarlo despues.
    op.create_unique_constraint("uq_users_email", 'users', ['email'])


def downgrade() -> None:
    """Downgrade schema."""

    # Ojo: el paso de minusculas NO se deshace. No hay forma de saber
    # que correos tenian mayusculas antes.

    op.drop_constraint("uq_users_email", 'users', type_='unique')

    op.alter_column('users', 'email',
        existing_type=sa.String(length=254),
        type_=sa.VARCHAR(length=40),
        existing_nullable=False)

    op.alter_column('tasks', 'title',
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=30),
        existing_nullable=False)