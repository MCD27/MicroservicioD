"""Inicializar tablas

Revision ID: adb4be760dec
Revises: 
Create Date: 2025-02-18 15:50:59.299765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adb4be760dec'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profesores',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('materia', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profesores_id'), 'profesores', ['id'], unique=False)
    op.create_table('estudiantes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('carrera', sa.String(), nullable=False),
    sa.Column('semestre', sa.Integer(), nullable=False),
    sa.Column('profesor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profesor_id'], ['profesores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_estudiantes_id'), 'estudiantes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_estudiantes_id'), table_name='estudiantes')
    op.drop_table('estudiantes')
    op.drop_index(op.f('ix_profesores_id'), table_name='profesores')
    op.drop_table('profesores')
    # ### end Alembic commands ###
