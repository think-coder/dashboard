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
    _sql_1 = """select distinct("work_province") from dashboard_data;"""
    res = execute_sql(conn, _sql_1)
    work_province_lst = [i.get("work_province") for i in res if i.get("work_province")]
    map_dict = {
        "上海市":"上海市",
        "云南省":"云南省",
        "内蒙古自治区":"内蒙古自治区",
        "北京市":"北京市",
        "吉林省":"吉林省",
        "四川省":"四川省",
        "天津市":"天津市",
        "宁夏自治区":"宁夏回族自治区",
        "安徽省":"安徽省",
        "山东省":"山东省",
        "山西省":"山西省",
        "广东省":"广东省",
        "广西省":"广西壮族自治区",
        "新疆自治区":"新疆维吾尔自治区",
        "江苏省":"江苏省",
        "江西省":"江西省",
        "河北省":"河北省",
        "河南省":"河南省",
        "浙江省":"浙江省",
        "海南省":"海南省",
        "湖北省":"湖北省",
        "湖南省":"湖南省",
        "甘肃省":"甘肃省",
        "福建省":"福建省",
        "西藏自治区":"西藏自治区",
        "贵州省":"贵州省",
        "辽宁省":"辽宁省",
        "重庆市":"重庆市",
        "陕西省":"陕西省",
        "青海省":"青海省",
        "黑龙江省":"黑龙江省"
    }
    for i in work_province_lst:
        if map_dict.get(i) != i and i is not None:
            print(map_dict.get(i), i)
            _sql_2 = """update dashboard_data set work_province='{workProvince_1}' where work_province='{workProvince_2}';""".format(workProvince_1=map_dict.get(i), workProvince_2=i)
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(_sql_2)
            conn.commit()
            cur.close()
    conn.close()

if __name__ == "__main__":
    main()
