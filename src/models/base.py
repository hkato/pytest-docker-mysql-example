from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import Config

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=create_engine(Config.get_database_url())
    )
)

Base = declarative_base()
Base.query = session.query_property()
