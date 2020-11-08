import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 環境変数から拾って切り替えとく
if os.getenv('MYSQL_USER'):
    dialect = 'mysql'
    driver = 'pymysql'
    user = os.getenv('MYSQL_USER', '')
    password = os.getenv('MYSQL_PASSWORD', '')
    host = os.getenv('MYSQL_HOST', '')
    database = os.getenv('MYSQL_DATABASE', '')
elif os.getenv('POSTGRES_USER'):
    dialect = 'postgresql'
    driver = 'psycopg2'
    user = os.getenv('POSTGRES_USER', '')
    password = os.getenv('POSTGRES_PASSWORD', '')
    host = os.getenv('POSTGRES_HOST', '')
    database = os.getenv('POSTGRES_DB', '')
else:
    raise Exception

# SQLAlchemy初期設定
engine = create_engine(
    '{}+{}://{}:{}@{}/{}'.format(
        dialect,
        driver,
        user,
        password,
        host,
        database
    )
)

Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = Session()


# モデルクラス郡を並べとく、あるいは別ファイルへ
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"autoload": True}


# とりあえのロジックね
def get_name_by_id(id):
    name = session.query(User).filter(User.id == id).first().name
    return name
