from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


db_admin = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///database.db'))

engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False})
Base = declarative_base()

