"""empty message

Revision ID: bfdc74116c5e
Revises: 
Create Date: 2019-08-13 12:15:43.212053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfdc74116c5e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=True),
    sa.Column('about_book', sa.String(length=150), nullable=True),
    sa.Column('author', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_book_author'), 'book', ['author'], unique=False)
    op.create_index(op.f('ix_book_title'), 'book', ['title'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('fio', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=150), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shelving', sa.Integer(), nullable=True),
    sa.Column('shelf', sa.Integer(), nullable=True),
    sa.Column('column', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_location_column'), 'location', ['column'], unique=False)
    op.create_index(op.f('ix_location_shelf'), 'location', ['shelf'], unique=False)
    op.create_index(op.f('ix_location_shelving'), 'location', ['shelving'], unique=False)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_table('status',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'book_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('status')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_location_shelving'), table_name='location')
    op.drop_index(op.f('ix_location_shelf'), table_name='location')
    op.drop_index(op.f('ix_location_column'), table_name='location')
    op.drop_table('location')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_book_title'), table_name='book')
    op.drop_index(op.f('ix_book_author'), table_name='book')
    op.drop_table('book')
    # ### end Alembic commands ###
