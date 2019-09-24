"""adding pitches

Revision ID: 33511124f953
Revises: 0d242b564373
Create Date: 2019-09-23 15:03:29.459516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33511124f953'
down_revision = '0d242b564373'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('cat_name', sa.String(length=255), nullable=True))
    op.drop_column('category', 'category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('category', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('category', 'cat_name')
    # ### end Alembic commands ###