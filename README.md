# データベースをDockerでfixtureするpytest環境例

## 目的

データベースを利用したPythonアプリのユニットテストをpytestで楽に環境の影響を受けず実行したい。(SQLite3等のファイルではなくデーモンとして立ち上がるもの)

## できたもの

サンプルコード: https://github.com/hkato/pytest-docker-mysql-example

pytestからMySQLをDocker上で立ち上げスキーマとテストデータを投入しテスト実行する。docker-composeの設定とdocker-entrypoint-initdb.dのSQL関連の対応をすればPostgreSQLなど他のデータベースでも基本同じはず。(docker-entrypoint-initdb.dでの初期化機構はMySQL/PostgreSQLのオフィシャルコンテナーは同様の動作のはずだが他は知らない)



## 必要な環境やpytest plugin

- Python3
  - pytest
  - pytest-docker
  - pytest-dotenv
- Docker

pytest関係で、Dockerを立ち上げたり、データベースを扱うプラグインを見てみたが、[pytest-docker](https://github.com/avast/pytest-docker)がメンテ状況や自分の用途・環境には良さそう。[pytest-dotenv](https://github.com/quiqua/pytest-dotenv)はDockerとpytestで環境変数を.envファイルに記述し共通化するために使用した。

### その他の検討

pytest-docker以外に多少検討してみたものとして、

- [pytest-docker-compose](https://github.com/pytest-docker-compose/pytest-docker-compose): 少し古い。pytest-dockerはdocker-composeを扱うのでメンテナンスやドキュメントがしっかりしたpytest-dockerの方が良いという印象。
- [pytest-dbfixtures](https://github.com/ClearcodeHQ/pytest-dbfixtures) シリーズ: 主流の各データーベースに対応
  - [pytest-mysql](https://github.com/ClearcodeHQ/pytest-mysql): ちゃんと見てないが、基本クライアントとして振る舞うので、Dockerの扱いが面倒そう。

結局、pytest-dockerはデータベースによらず、公式ドキュメントにあるようにWebアプリのコンテナーを使ったり、汎用的に利用できるので一番良さそう([MinIOのコンテナーを起動しAWS S3代わり](https://qiita.com/hkato/items/89e436300c50c46624b9)にもしようと思っている)。

## ディレクトリ構成

```text
.
├── src                 # アプリケーションコード
│   └── *.py
├── tests               # テストコード
│   ├── conftest.py
│   └── test_*.py
├── initdb.d            # データーベーススキーマ＆テストデータなど
│   ├── *.sql
│   └── *.sh
├── pytest.ini          # pytest設定
├── .env                # 環境変数設定
└── docker-compose.yml  # Docker設定
```

## コード概要

### conftest.py

#### docker-compose.ymlの配置対応

pytest-dockerはデフォルトで `tests/` の下の `docker-compose.yml` を参照する。プロジェクト直下に設定することにより(別ディレクトリやファイル名の指定はpytest-dockerのREADME.mdにサンプルにあり)、Webアプリなどの場合は `docker-compose up -d` してデータベースを動かしつつ、Gunicorn, uWSGI, UvicornなどでWebアプリサーバーを実行してデバッグできる(今回の本質ではないのでこれは除いている)。

#### MySQL起動待ち対応

pytest-dockerのドキュメントでは[httpbin](https://httpbin.org)のREST APIのコンテナーを立ち上げて、80ポートから200応答が帰るのを待つサンプルとして記述されている。MySQLの場合は下記のようにPyMySQLで接続しExceptionが帰ってこない、つまりDockerコンテナーが立ち上がり、初期データが投入完了したという判断にした。

```python
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
```

上記をで0.1秒周期で30秒タイムアウトで待つ。

```python
@pytest.fixture(scope="session")
def database_service(docker_ip, docker_services):
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_database_ready(docker_ip)
    )
    return
```

#### 実行結果

初期設定

```sh
$ # 実際の運用ではテスト環境と実行環境のためPipenvとかPoetryを使うのが良いかも
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

テスト実行するとFixtureでDockerコンテナーを起動し、そのコンテナー内のdocker-entrypoint-initdb.dの機構によりSQLやシェルスクリプトなどが適用されてた後に実際のユニットテストが実行される。

```sh
$ pytest
============================= test session starts ==============================
platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1 -- /Users/username/tmp/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/username/tmp, configfile: pytest.ini
plugins: dotenv-0.5.2, cov-2.10.1, docker-0.10.1
collected 1 item                                                               

tests/test_users.py::test_get_name_by_id PASSED                          [100%]

---------- coverage: platform darwin, python 3.8.6-final-0 -----------
Name         Stmts   Miss  Cover
--------------------------------
src/app.py       8      0   100%


============================== 1 passed in 16.35s ==============================
```

## まとめ

- pytest-dockerはデータベースに限らずテストに依存するサービスをDockerで立ち上げるられるので便利
- docker-compose.ymlの配置位置をtests/からプロジェクト直下に変えると良いかも。通常のデバッグにも使える
- docker_services.wait_until_responsive()にコンテナーの内容に合わせた起動待ち処理を実装する
