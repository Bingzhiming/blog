"""empty message

Revision ID: a3114a68ff6c
Revises: 
Create Date: 2019-03-07 11:51:21.280340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3114a68ff6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('permission', sa.Integer(), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('label', sa.String(length=128), nullable=True),
    sa.Column('location', sa.String(length=32), nullable=True),
    sa.Column('register_time', sa.DateTime(), nullable=True),
    sa.Column('login_time', sa.DateTime(), nullable=True),
    sa.Column('last_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('follows',
    sa.Column('fensi_id', sa.Integer(), nullable=False),
    sa.Column('dav_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['dav_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['fensi_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('fensi_id', 'dav_id')
    )
    op.create_table('collects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('collector_id', sa.Integer(), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['collector_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('collects')
    op.drop_table('follows')
    op.drop_table('blogs')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
