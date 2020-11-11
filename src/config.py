import os

DB_ENV = {
    'mysql': {
        'user': 'MYSQL_USER',
        'password': 'MYSQL_PASSWORD',
        'host': 'MYSQL_HOST',
        'database': 'MYSQL_DATABASE'
    },
    'postgresql': {
        'user': 'POSTGRES_USER',
        'password': 'POSTGRES_PASSWORD',
        'host': 'POSTGRES_HOST',
        'database': 'POSTGRES_DB'
    }
}


class Config:
    @classmethod
    def get_database_url(self):
        # 環境変数の *_USER でどのデータベースか切り替え値を切り替えとく
        if os.getenv('MYSQL_USER'):
            dialect, driver = 'mysql', 'pymysql'
        elif os.getenv('POSTGRES_USER'):
            dialect, driver = 'postgresql', 'psycopg2'
        else:
            raise Exception('Database environ is not defined.')

        url = '{}+{}://{}:{}@{}/{}'.format(
            dialect, driver,
            os.getenv(DB_ENV[dialect]['user']),
            os.getenv(DB_ENV[dialect]['password']),
            os.getenv(DB_ENV[dialect]['host']),
            os.getenv(DB_ENV[dialect]['database'])
        )

        return url
