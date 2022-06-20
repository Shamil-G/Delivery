import psycopg2 as pgsql
from psycopg2 import OperationalError, pool
import db_config as cfg
from main_app import log

st_log = 'create table if not exists service_log(order_num varchar(12) primary key, ' \
         'date_order timestamp, date_delivery date, service_name varchar(32), iin char(12), ' \
         'status varchar(64), type varchar(132), status_delivery varchar(64))'

try:
    _pool = pgsql.pool.SimpleConnectionPool(cfg.db_min_connection, cfg.db_max_connection,
                                            database=cfg.database,
                                            user=cfg.db_user,
                                            password=cfg.db_password,
                                            host=cfg.db_host)
    print('Connection POOL was created')
except OperationalError as error:
    print(f'Ошибка создания пула соединений к БД {cfg.database} : {error}')


def get_connect():
    if _pool:
        # print('Получаем соединение из POOL')
        return _pool.getconn()
    else:
        return None


def add_init_record(order_num, service_name, iin, status, type):
    try:
        conn = get_connect()
        with conn.cursor() as cursor:
            stmt = f"insert into service_log(order_num, date_order, service_name, iin, status, type) " \
                   f"values('{order_num}', clock_timestamp(), '{service_name}', '{iin}', '{status}', '{type}')"
            print(f"--> ADD INIT RECORD to {cfg.database} on {cfg.db_host}: {stmt}")
            log.info(f"--> ADD INIT RECORD to {cfg.database} on {cfg.db_host}: {stmt}")
            cursor.execute(stmt)
            cursor.execute('commit')
    except Exception as e2:
        log.info(e2)
    finally:
        _pool.putconn(conn)


def add_service_record(order_num, service_name, iin, status, type):
    try:
        conn = get_connect()
        with conn.cursor() as cursor:
            stmt = f"insert into service_log(order_num, date_order, service_name, iin, status, type) " \
                   f"values('{order_num}', clock_timestamp(), '{service_name}', '{iin}', '{status}', '{type}')"
            print(f"--> ADD SERVICE RECORD to {cfg.database} on {cfg.db_host}: {stmt}")
            cursor.execute(stmt)
            log.info(f"--> ADD SERVICE RECORD to {cfg.database} on {cfg.db_host}: {stmt}")
            cursor.execute('commit')
    except Exception as e2:
        log.info(e2)
    finally:
        _pool.putconn(conn)


def create_log():
    try:
        conn = get_connect()
        with conn.cursor() as cursor:
            cursor.execute('drop table service_log')
            cursor.execute('commit')
            cursor.execute(st_log)
    except Exception as e2:
        log.info(e2)
    finally:
        _pool.putconn(conn)


def select(stmt):
    sel_rec = []
    try:
        conn = get_connect()
        with conn.cursor() as cursor:
            print(f"Выбираем данные: {stmt}")
            cursor.execute(stmt)
            sel_rec = cursor.fetchall()
    finally:
        _pool.putconn(conn)
        return sel_rec


if __name__ == "__main__":
    # create_log()
    # add_init_record('222333', 'Yandex', '630112300169', 'direct', 'Справка об отсутствии судимости')
    # add_init_record('333444', 'Yandex', '630112300169', 'direct', 'Справка о адресе проживания')
    # add_init_record('444555', 'myKhat', '630112300169', 'direct', 'Справка о рождении')
    # print(f"Добавили записи ...")
    records = select('select * from service_log')
    records = select('select * from service_log')
    records = select('select * from service_log')
    for _ in records:
        print(f"{_}")
