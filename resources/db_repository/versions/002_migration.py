from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menus = Table('menus', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('parent_code', String(length=32)),
    Column('menu_code', String(length=32), nullable=False),
    Column('menu_name', String(length=64), nullable=False),
    Column('menu_url', String(length=255)),
    Column('describe', String(length=255)),
    Column('ext', String(length=255)),
    Column('last_date', DateTime, nullable=False),
    Column('version', Integer, nullable=False, default=ColumnDefault(1)),
)

resources = Table('resources', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('resource_code', String(length=32), nullable=False),
    Column('resource_name', String(length=64), nullable=False),
    Column('resource_url', String(length=255)),
    Column('describe', String(length=255)),
    Column('ext', String(length=255)),
    Column('last_date', DateTime, nullable=False),
    Column('version', Integer, nullable=False, default=ColumnDefault(1)),
)

role_menus = Table('role_menus', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('role_code', Integer, nullable=False),
    Column('menu_code', String(length=32), nullable=False),
    Column('last_date', DateTime, nullable=False),
)

role_resources = Table('role_resources', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('role_code', Integer, nullable=False),
    Column('resource_code', String(length=32), nullable=False),
    Column('last_date', DateTime, nullable=False),
)

user_menus = Table('user_menus', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('menu_code', String(length=32), nullable=False),
    Column('last_date', DateTime, nullable=False),
)

user_resources = Table('user_resources', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('resource_code', String(length=32), nullable=False),
    Column('last_date', DateTime, nullable=False),
)

user_roles = Table('user_roles', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('role_code', String(length=32), nullable=False),
    Column('last_date', DateTime, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menus'].create()
    post_meta.tables['resources'].create()
    post_meta.tables['role_menus'].create()
    post_meta.tables['role_resources'].create()
    post_meta.tables['user_menus'].create()
    post_meta.tables['user_resources'].create()
    post_meta.tables['user_roles'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menus'].drop()
    post_meta.tables['resources'].drop()
    post_meta.tables['role_menus'].drop()
    post_meta.tables['role_resources'].drop()
    post_meta.tables['user_menus'].drop()
    post_meta.tables['user_resources'].drop()
    post_meta.tables['user_roles'].drop()
