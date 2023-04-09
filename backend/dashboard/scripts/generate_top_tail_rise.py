import os
import psycopg2
import psycopg2.extras
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED

CONST = {
    "_sql_title_2017": """
        SELECT DISTINCT(title) FROM "data" WHERE "year"='2017' AND "work_province"='{_province}'; 
    """,
    "_sql_title_2021": """
        SELECT DISTINCT(title) FROM "data" WHERE "year"='2021' AND "work_province"='{_province}'; 
    """,
    "_sql_mix": """
        SELECT ROUND(
            (SELECT COUNT(*) FROM "data" WHERE "year"='2021' AND "work_province"='{_province}' AND "title"='{_title}')
            /
            (SELECT CASE WHEN COUNT(*)=0 THEN 1 ELSE COUNT(*) END FROM "data" WHERE "year"='2017' AND "work_province"='{_province}' AND "title"='{_title}')
            ^
            0.25
            -
            1
        )
    """,
    "_sql_all_province": """
        SELECT DISTINCT(province) FROM province_maptype
    """,
    "_sql_insert_data": """
        INSERT INTO {_table} VALUES ({_id}, '{_title}', {_percentage})
    """
}

CONST_MAP_PERCENT = {
    "新疆维吾尔自治区": "per_title_xinjiang",
    "青海省": "per_title_qinghai",
    "湖北省": "per_title_hubei",
    "山西省": "per_title_shanxi_1",
    "云南省": "per_title_yunnan",
    "河北省": "per_title_hebei",
    "广西壮族自治区": "per_title_guangxi",
    "海南省": "per_title_hainan",
    "上海市": "per_title_shanghai",
    "辽宁省": "per_title_liaoning",
    "福建省": "per_title_fujian",
    "陕西省": "per_title_shanxi_2",
    "四川省": "per_title_sichuan",
    "贵州省": "per_title_guizhou",
    "广东省": "per_title_guangdong",
    "北京市": "per_title_beijing",
    "黑龙江省": "per_title_heilongjiang",
    "江苏省": "per_title_jiangsu",
    "天津市": "per_title_tianjin",
    "重庆市": "per_title_chongqing",
    "山东省": "per_title_shandong",
    "内蒙古自治区": "per_title_neimenggu",
    "宁夏回族自治区": "per_title_ningxia",
    "浙江省": "per_title_zhejiang",
    "西藏自治区": "per_title_xizang",
    "吉林省": "per_title_jilin",
    "安徽省": "per_title_anhui",
    "江西省": "per_title_jiangxi",
    "甘肃省": "per_title_gansu",
    "河南省": "per_title_henan",
    "湖南省": "per_title_hunan"
}

CONST_MAP_PROVINCE = {
    "新疆维吾尔自治区": "xinjiang",
    "青海省": "qinghai",
    "湖北省": "hubei",
    "山西省": "shanxi_1",
    "云南省": "yunnan",
    "河北省": "hebei",
    "广西壮族自治区": "guangxi",
    "海南省": "hainan",
    "上海市": "shanghai",
    "辽宁省": "liaoning",
    "福建省": "fujian",
    "陕西省": "shanxi_2",
    "四川省": "sichuan",
    "贵州省": "guizhou",
    "广东省": "guangdong",
    "北京市": "beijing",
    "黑龙江省": "heilongjiang",
    "江苏省": "jiangsu",
    "天津市": "tianjin",
    "重庆市": "chongqing",
    "山东省": "shandong",
    "内蒙古自治区": "neimenggu",
    "宁夏回族自治区": "ningxia",
    "浙江省": "zhejiang",
    "西藏自治区": "xizang",
    "吉林省": "jilin",
    "安徽省": "anhui",
    "江西省": "jiangxi",
    "甘肃省": "gansu",
    "河南省": "henan",
    "湖南省": "hunan"
}

def main_logic(province):
    print(province)
    conn = psycopg2.connect(
        database='dashboard',
        user='postgres',
        password='cG9zdGdyZXM=',
        host='localhost',
        port='55432',
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(CONST.get("_sql_title_2017").format(
        _province=province
    ))
    result_2017 = cur.fetchall()
    cur.execute(CONST.get("_sql_title_2021").format(
        _province=province
    ))
    result_2021 = cur.fetchall()
    conn.commit()
    totle_tile = list(set(
        [i.get("title") for i in result_2017] + 
        [i.get("title") for i in result_2021]
    ))

    _num = 1
    for title in totle_tile:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(CONST.get("_sql_mix").format(
            _province=province, _title=title
        ))
        result = cur.fetchall()
        cur.execute(CONST.get("_sql_insert_data").format(
            _table=CONST_MAP_PERCENT.get(province),
            _id=_num, 
            _title=title, 
            _percentage=int(result[0].get("round"))
        ))
        conn.commit()
        cur.close()
        print(os.getpid(), province, title, result[0].get("round"))
        _num += 1


if __name__ == "__main__":
    conn = psycopg2.connect(
        database='dashboard',
        user='postgres',
        password='cG9zdGdyZXM=',
        host='localhost',
        port='55432',
    )

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(CONST.get("_sql_all_province"))
    result = cur.fetchall()
    cur.close()
    province_list = [i.get("province") for i in result]
    # conn.close()

    process_pool = ProcessPoolExecutor(max_workers=8)
    all_task = [process_pool.submit(main_logic, (province)) for province in province_list]
    wait(all_task, return_when=ALL_COMPLETED)
    process_pool.shutdown()

    # main_logic("青海省")

