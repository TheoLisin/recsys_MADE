"""migrate to postgresql

Revision ID: b77054f8e49e
Revises: 
Create Date: 2022-11-27 01:48:18.664034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b77054f8e49e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=64), nullable=True),
    sa.Column('pwdhash', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('login_ind', 'users', ['login'], unique=False)
    op.create_table('venues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('old_id', sa.String(length=64), nullable=True),
    sa.Column('raw_en', sa.String(length=1024), nullable=True),
    sa.Column('sid', sa.String(length=256), nullable=True),
    sa.Column('name_d', sa.String(length=256), nullable=True),
    sa.Column('type', sa.String(length=8), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_venue', sa.Integer(), nullable=True),
    sa.Column('old_id', sa.String(length=64), nullable=True),
    sa.Column('title', sa.String(length=2048), nullable=True),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('n_citation', sa.Integer(), nullable=True),
    sa.Column('article_len', sa.Integer(), nullable=True),
    sa.Column('lang', sa.String(length=4), nullable=True),
    sa.Column('issn', sa.String(length=1024), nullable=True),
    sa.Column('keywords', sa.Text(), nullable=True),
    sa.Column('isbn', sa.String(length=64), nullable=True),
    sa.Column('abstract', sa.Text(), nullable=True),
    sa.Column('has_doi', sa.Boolean(), nullable=True),
    sa.Column('fos', sa.String(length=1024), nullable=True),
    sa.ForeignKeyConstraint(['id_venue'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('year_ind', 'articles', ['year'], unique=False)
    op.create_table('authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('old_id', sa.String(length=64), nullable=True),
    sa.Column('gid', sa.String(length=32), nullable=True),
    sa.Column('sid', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=512), nullable=True),
    sa.Column('organisation', sa.String(length=2048), nullable=True),
    sa.Column('orgid', sa.String(length=128), nullable=True),
    sa.Column('orgs_count', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=512), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article_author',
    sa.Column('id_article', sa.Integer(), nullable=False),
    sa.Column('id_author', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_article'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['id_author'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id_article', 'id_author')
    )
    op.create_table('article_tags',
    sa.Column('id_article', sa.Integer(), nullable=False),
    sa.Column('id_tag', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_article'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['id_tag'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('id_article', 'id_tag')
    )
    op.create_table('coauthors',
    sa.Column('id_author', sa.Integer(), nullable=False),
    sa.Column('id_coauth', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_author'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['id_coauth'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id_author', 'id_coauth')
    )
    op.create_table('references',
    sa.Column('id_where', sa.Integer(), nullable=False),
    sa.Column('id_what', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_what'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['id_where'], ['articles.id'], ),
    sa.PrimaryKeyConstraint('id_where', 'id_what')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('references')
    op.drop_table('coauthors')
    op.drop_table('article_tags')
    op.drop_table('article_author')
    op.drop_table('authors')
    op.drop_index('year_ind', table_name='articles')
    op.drop_table('articles')
    op.drop_table('venues')
    op.drop_index('login_ind', table_name='users')
    op.drop_table('users')
    op.drop_table('tags')
    # ### end Alembic commands ###
