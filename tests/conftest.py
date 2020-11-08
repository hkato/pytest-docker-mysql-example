import os
import sys

try:
    import psycopg2
except:
    pass
try:
    import pymysql
except:
    pass
import pytest


# src/にパスを通し テストコード側は、
# from src.foo import bar でなく from app import bar で良くする
sys.path.append(os.path.abspath(os.path.dirname(
    os.path.abspath(__file__)) + "/../src/"))


# 接続を試みて、Exceptionが発生しなくなったらコンテナー起動済みとしてる
def is_mysqld_ready(docker_ip):
    try:
        pymysql.connect(
            user=os.getenv('MYSQL_USER', ''),
            password=os.getenv('MYSQL_PASSWORD', ''),
            host=docker_ip,
            db=os.getenv('MYSQL_DATABASE', '')
        )
        return True
    except:
        return False


def is_postgresql_ready(docker_ip):
    try:
        psycopg2.connect(
            "postgresql://{user}:{password}@{host}/{db}".format(
                user=os.getenv('POSTGRES_USER', ''),
                password=os.getenv('POSTGRES_PASSWORD', ''),
                host=docker_ip,
                db=os.getenv('POSTGRES_DB', '')
            )
        )
        return True
    except:
        return False


# MySQLとPostgreSQL切り替え コンテナー立ち上がり待ち
if os.getenv('MYSQL_USER'):
    is_database_ready = is_mysqld_ready
    compose_file = 'docker-compose.yml'
elif os.getenv('POSTGRES_USER'):
    is_database_ready = is_postgresql_ready
    compose_file = 'docker-compose-postgres.yml'
else:
    raise Exception('Database type is not defined.')


# pytest-dockerはデフォルトで　tests/ の下の docker-compose.yml を参照するので
# カスタム設定でプロジェクトルートのものを参照
# これによりWebアプリなどの場合 docker-compose up -d しつつ、
# Gunicorn, uWSGIm UvicornなどでWebアプリサーバーを動かしつつデバッグできる
@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), compose_file)


@pytest.fixture(scope="session")
def database_service(docker_ip, docker_services):
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_database_ready(docker_ip)
    )
    return
