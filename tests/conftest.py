import os
import sys

import pymysql
import pytest

# src/にパスを通し テストコード側は、
# from src.foo import bar でなく from app import bar で良くする
sys.path.append(os.path.abspath(os.path.dirname(
    os.path.abspath(__file__)) + "/../src/"))


# pytest-dockerはデフォルトで　tests/ の下の docker-compose.yml を参照するので
# カスタム設定でプロジェクトルートのものを参照
# これによりWebアプリなどの場合 docker-compose up -d しつつ、
# Gunicorn, uWSGIm UvicornなどでWebアプリサーバーを動かしつつデバッグできる
@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "docker-compose.yml")


# 接続を試みて、Exceptionが発生しなくなったらコンテナー起動済みとしてる
def is_database_ready(docker_ip):
    try:
        pymysql.connect(
            host=docker_ip,
            user=os.getenv('MYSQL_USER', ''),
            password=os.getenv('MYSQL_PASSWORD', ''),
            db=os.getenv('MYSQL_DATABASE')
        )
        return True
    except:
        return False


@pytest.fixture(scope="session")
def database_service(docker_ip, docker_services):
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_database_ready(docker_ip)
    )
    return
