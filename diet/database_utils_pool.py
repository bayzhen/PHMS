import pymysql
from dbutils.pooled_db import PooledDB

dependency_pool = PooledDB(
    creator=pymysql,
    maxconnections=None,
    mincached=2,
    maxcached=None,
    maxshared=3,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=None,
    host='101.35.143.22',
    port=3306,
    user="PHMS",
    password="123456",
    database="phms",
    charset='utf8'
)


class DatabasePool:

    def __init__(self):
        self.pool = dependency_pool

    def create_conn_cursor(self):
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor

    def fetchall(self, sql):
        conn, cursor = self.create_conn_cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def fetchone(self, sql):
        conn, cursor = self.create_conn_cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def insert(self, sql):
        conn, cursor = self.create_conn_cursor()
        state = True
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print('insert error :' + str(e))
            state = False
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        return state

    def update(self, sql: object) -> object:
        conn, cursor = self.create_conn_cursor()
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print('update error :' + str(e))
            conn.rollback()
        finally:
            cursor.close()
            conn.close()









