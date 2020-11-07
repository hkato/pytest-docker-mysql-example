import os

import pymysql


def get_name_by_id(id):
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST', '127.0.0.1'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        db=os.getenv('MYSQL_DATABASE', ''),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT id, name FROM users where id = %s',
            id
        )

        result = cursor.fetchone()

        return result['name']
