# -*- coding:utf-8 -*-

import psycopg2
import psycopg2.extras

def get_connect():
    conn = psycopg2.connect(
        database='dashboard',
        user='postgres',
        password='postgres',
        host='127.0.0.1',
        port='15432',
    )
    return conn


def main():
    conn_a = psycopg2.connect(
        database='dashboard',
        user='postgres',
        password='postgres',
        host='127.0.0.1',
        port='5432',
    )
    conn_b = psycopg2.connect(
        database='backend',
        user='postgres',
        password='postgres',
        host='127.0.0.1',
        port='5432',
    )
    cur_a = conn_a.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur_b = conn_b.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    _sql_a = """
        SELECT id, city, province FROM dashboard_province_city_map;
    """
    _sql_b = """
        INSERT INTO province_city_map (id, city, province) VALUES ({_id}, '{_city}', '{_province}');
    """
    cur_a.execute(_sql_a)
    result = cur_a.fetchall()
    conn_a.commit()
    cur_a.close()
    j = 1
    for i in result:
        if not i.get("id"):
            continue
        print(_sql_b.format(_id=i.get("id"), _city=i.get("city"), _province=i.get("province")))
        cur_b.execute(_sql_b.format(_id=i.get("id"), _city=i.get("city"), _province=i.get("province")))
        conn_b.commit()
        j += 1
    cur_b.close()
    conn_a.close()
    conn_b.close()


if __name__ == "__main__":
    main()
