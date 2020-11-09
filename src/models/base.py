from config import Config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=Config.get_engine()
    )
)

Base = declarative_base()
Base.query = session.query_property()
