import psycopg2 as pgsql
from psycopg2 import OperationalError, pool


st_log = 'create table service_log(id serial primary key, ' \
         'date_op timestamp, service_name varchar(32), iin char(12), status varchar(64))'

try:
    _pool = pgsql.pool.SimpleConnectionPool(1, 5,
                            database='delivery',
                            user='delivery',
                            password='delivery',
                            host='10.51.203.159')
except OperationalError as error:
    print('Ошибка подключения к БД')


def get_connect():
    if _pool:
        print('Connection POOL was created')
        return _pool.getconn()
    else:
        return None


def create_log():
    with get_connect().cursor() as cursor:
        cursor.execute('drop table service_log')
        cursor.execute(st_log)
        cursor.execute('insert into service_log(date_op, service_name, iin, status) '
                       "values(clock_timestamp (), 'clock_timestamp', '630112300169', 'NO ORDER')  ")

        cursor.execute('insert into service_log(date_op, service_name, iin, status) '
                       "values(now(), 'now', '630112300169', 'NO ORDER')  ")

        cursor.execute('insert into service_log(date_op, service_name, iin, status) '
                       "values(current_timestamp, 'current_timestamp', '630112300169', 'NO ORDER')  ")

        cursor.execute('commit')
        cursor.execute("select id, to_char(date_op, 'YYYY-MM-DD HH24:MI:SS'), "
                       "service_name, iin, status from service_log")
        rec = cursor.fetchall()

        cursor.close()
        return rec


def select(stmt):
    with get_connect().cursor() as cursor:
        cursor.execute(stmt)
        rec = cursor.fetchall()
        cursor.close()
        return rec


if __name__ == "__main__":
    records = create_log()
    # record = select('select * from service_log')
    # record = select("select version()")
    for rec in records:
        print(f"Подключились {rec}")
