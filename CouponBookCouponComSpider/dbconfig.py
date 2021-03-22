import mysql.connector
import configparser

DB_CONN_POOL_NAME = "passbook_pool"

config = configparser.ConfigParser()
config.read('../config.ini')

dbconfig = {
    "host": config['mysqlDB']['host'],
    "database": config['mysqlDB']['database'],
    "user": config['mysqlDB']['user'],
    "password": config['mysqlDB']['password']
}


def init_db_conn_pool():
    mysql.connector.connect(pool_name=DB_CONN_POOL_NAME,
                            pool_size=3,
                            **dbconfig)


def get_db_conn():
    return mysql.connector.connect(pool_name=DB_CONN_POOL_NAME)
