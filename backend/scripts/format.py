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

def execute_sql(conn, sql):
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    return result

def main():
    conn = get_connect()
    _sql = """select distinct("workLocation") from dashboard_data_copy1;"""
    res = execute_sql(conn, _sql)
    work_location_list = [i.get("workLocation") for i in res if i.get("workLocation")]
    for i in work_location_list:
        _sql_1 = """select province,city from province_city_map where city like '%{city}%'""".format(city=i)
        res = execute_sql(conn, _sql_1)
        if not res:
            continue
        _sql_2 = """update dashboard_data_copy1 set workLocation='{worklocation}', workProvince='{workProvince}' where workLocation='{item}'""".format(worklocation=res[0].get("city"), workProvince=res[0].get("province"), item=i)
        print(_sql_2)
        res = execute_sql(conn, _sql_2)




if __name__ == "__main__":
    main()
