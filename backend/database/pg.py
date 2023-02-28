# -*- coding:utf-8 -*-
import os

import configparser
import psycopg2
import psycopg2.extras

def get_connect():
    _list = os.path.dirname(os.path.abspath(__file__)).split("/")[0:-1]
    _list.append("config")
    _list.append("db.ini")
    ini_path = "/".join(_list)

    configer = configparser.ConfigParser()
    configer.read(ini_path)
    pg_config = configer["postgresql"]

    conn = psycopg2.connect(
        database=pg_config["database"],
        user=pg_config["user"],
        password=pg_config["password"],
        host=pg_config["host"],
        port=pg_config["port"],
    )
    return conn

def execute_sql(conn, sql):
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    return result
