"""add foreign keys to events

Revision ID: 2cfad1e9d864
Revises: 2b3f98dfa272
Create Date: 2025-11-25 19:48:39.051806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cfad1e9d864'
down_revision: Union[str, Sequence[str], None] = '2b3f98dfa272'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # 1. Добавляем новые поля id
    op.add_column(
        'events',
        sa.Column('category_id', sa.Integer(), nullable=False)
    )
    op.add_column(
        'events',
        sa.Column('author_id', sa.Integer(), nullable=False)
    )

    # 2. Создаём внешние ключи
    op.create_foreign_key(
        'fk_events_category',
        'events',
        'category',          # имя таблицы категорий
        ['category_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_events_author',
        'events',
        'users',             # имя таблицы пользователей
        ['author_id'],
        ['id']
    )

    # 3. Удаляем старые текстовые поля
    op.drop_column('events', 'category')
    op.drop_column('events', 'Author')


def downgrade() -> None:

    # ОТКАТ: вернуть старые поля
    op.add_column('events', sa.Column('Author', sa.String(length=255)))
    op.add_column('events', sa.Column('category', sa.String(length=255)))

    # удалить внешние ключи
    op.drop_constraint('fk_events_author', 'events', type_='foreignkey')
    op.drop_constraint('fk_events_category', 'events', type_='foreignkey')

    op.drop_column('events', 'author_id')
    op.drop_column('events', 'category_id')