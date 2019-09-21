from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
roles = Table('roles', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('role_code', String(length=32), nullable=False),
    Column('role_name', String(length=64), nullable=False),
    Column('describe', String(length=255)),
    Column('ext', String(length=255)),
    Column('last_date', DateTime, nullable=False),
    Column('version', Integer, nullable=False, default=ColumnDefault(1)),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64), nullable=False),
    Column('password', String(length=64), nullable=False),
    Column('email', String(length=64), nullable=False),
    Column('qq', String(length=20)),
    Column('is_available', Integer, nullable=False, default=ColumnDefault(1)),
    Column('ext', String(length=255)),
    Column('last_date', DateTime, nullable=False),
    Column('version', Integer, nullable=False, default=ColumnDefault(1)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['roles'].create()
    post_meta.tables['users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['roles'].drop()
    post_meta.tables['users'].drop()
