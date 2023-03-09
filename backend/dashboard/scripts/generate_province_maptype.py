# -*- coding:utf-8 -*-

import psycopg2
import psycopg2.extras

def main():
    province_maptype = {
        "新疆维吾尔自治区": "新疆",
        "青海省": "青海",
        "湖北省": "湖北",
        "山西省": "山西",
        "云南省": "云南",
        "河北省": "河北",
        "广西壮族自治区": "广西",
        "海南省": "海南",
        "上海市": "上海",
        "辽宁省": "辽宁",
        "福建省": "福建",
        "陕西省": "陕西",
        "四川省": "四川",
        "贵州省": "贵州",
        "广东省": "广东",
        "北京市": "北京",
        "黑龙江省": "黑龙江",
        "江苏省": "江苏",
        "天津市": "天津",
        "重庆市": "重庆",
        "山东省": "山东",
        "内蒙古自治区": "内蒙古",
        "宁夏回族自治区": "宁夏",
        "浙江省": "浙江",
        "西藏自治区": "西藏",
        "吉林省": "吉林",
        "安徽省": "安徽",
        "江西省": "江西",
        "甘肃省": "甘肃",
        "河南省": "河南",
        "湖南省": "湖南"
    }
    conn = psycopg2.connect(
        database='dashboard',
        user='postgres',
        password='postgres',
        host='172.19.125.144',
        port='15432',
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    _sql = """
        INSERT INTO province_maptype (id, province, maptype) VALUES ({_id}, '{province}', '{maptype}');
    """
    _id = 1
    for k, v in province_maptype.items():
        cur.execute(_sql.format(_id=_id, province=k, maptype=v))
        _id += 1
        print(_sql.format(_id=_id, province=k, maptype=v))
        conn.commit()

    cur.close()
    conn.close()
        

if __name__ == "__main__":
    main()
