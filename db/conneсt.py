import psycopg2 as pgsql
from psycopg2 import OperationalError, pool
import db_config as cfg
from util.logger import log

st_create_table = 'create table if not exists service_log(order_num varchar(12), ' \
         'date_create timestamp default current_timestamp, date_delivery timestamp, region_code varchar(12), ' \
         'service_name varchar(32), iin char(12), ' \
         'status varchar(64), type varchar(256), status_delivery varchar(64))'

st_create_index = 'create unique index if not exists pk_service_log on public.service_log(order_num, service_name)'

try:
    _pool = pgsql.pool.SimpleConnectionPool(cfg.db_min_connection, cfg.db_max_connection,
                                            database=cfg.database,
                                            user=cfg.db_user,
                                            password=cfg.db_password,
                                            host=cfg.db_host)
    print('Connection POOL had created')
except OperationalError as error:
    print(f'Ошибка создания пула соединений к БД {cfg.database} : {error}')


def get_connect():
    if _pool:
        # print('Получаем соединение из POOL')
        return _pool.getconn()
    else:
        return None


def add_init_record(order_num, region_code, service_name, iin, status, type):
    try:
        conn = get_connect()
        with conn.cursor() as cursor:
            stmt = f"insert into service_log(order_num, region_code, service_name, iin, status, type) " \
                   f"values('{order_num}', '{region_code}', '{service_name}', '{iin}', '{status}', '{type}')"
            log.info(f"ADD RECORD to Database: {cfg.database}, Host: {cfg.db_host}: {stmt}")
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
            cursor.execute(stmt)
            log.info(f"ADD SERVICE RECORD to Database: {cfg.database}, Host: {cfg.db_host}: {stmt}")
            cursor.execute('commit')
    except Exception as e2:
        log.info(e2)
    finally:
        _pool.putconn(conn)


def create_table_service_log():
    try:
        conn = get_connect()
        with conn.cursor() as cursor:
            # cursor.execute('drop table service_log')
            cursor.execute(st_create_table)
            cursor.execute(st_create_index)
            cursor.execute('commit')
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
    create_table_service_log()
    # add_init_record('222333', '12345', 'Yandex', '630112300169', 'direct', 'Справка об отсутствии судимости')
    # add_init_record('333444', 'Yandex', '630112300169', 'direct', 'Справка о адресе проживания')
    # add_init_record('444555', 'myKhat', '630112300169', 'direct', 'Справка о рождении')
    # print(f"Добавили записи ...")
    # records = select('select * from service_log')
    # records = select('select * from service_log')
    records = select('select * from service_log')
    for _ in records:
        print(f"{_}")
