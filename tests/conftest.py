import os

import pytest

from myapp.models.base import session


def is_database_ready(docker_ip):
    """データベース起動待ち
    接続を試みて、Exceptionが発生しなくなったらコンテナー起動済みとする
    MySQL/PostgreSQLはSELECT version()でバージョン応答できるのでこれで試しとく
    """
    try:
        session.execute("SELECT version()")
        return True
    except:
        return False


@pytest.fixture(scope='session')
def docker_compose_file(pytestconfig):
    """Docker Composeの設定ファイルを返す
    pytest-dockerはデフォルトで　`tests/` の下の `docker-compose.yml` を参照するので
    カスタム設定でプロジェクトルートのものを参照させる
    これによりWebアプリなどの場合 `docker-compose up -d` しつつ、
    Gunicorn, uWSGIm UvicornなどでWebアプリサーバーを動かしつつデバッグできる
    """
    return os.path.join(str(pytestconfig.rootdir), os.getenv('COMPOSE_FILE', 'docker-compose.yml'))


@pytest.fixture(scope='session')
def database_service(docker_ip, docker_services):
    """Docker database service 起動待ち"""
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_database_ready(docker_ip)
    )
