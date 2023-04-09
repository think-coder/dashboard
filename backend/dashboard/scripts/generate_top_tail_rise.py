import os
import psycopg2
import psycopg2.extras
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED

CONST = {
    "_sql_title_2017": """
        SELECT DISTINCT(title) FROM "data" WHERE "year"='2017' AND "work_province"='{province}'; 
    """,
    "_sql_title_2021": """
        SELECT DISTINCT(title) FROM "data" WHERE "year"='2021' AND "work_province"='{province}'; 
    """,
    "_sql_mix": """
        SELECT ROUND(
            (SELECT COUNT(*) FROM "data" WHERE "year"='2021' AND "work_province"='{province}' AND "title"='{title}')
            /
            (SELECT CASE WHEN COUNT(*)=0 THEN 1 ELSE COUNT(*) END FROM "data" WHERE "year"='2017' AND "work_province"='{province}' AND "title"='{title}')
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
        INSERT INTO per_title VALUES ({_id}, {_title}, {_percentage})
    """
}

def main(province):
    conn = psycopg2.connect(
        database='dashboard',
        user='postgres',
        password='cG9zdGdyZXM=',
        host='localhost',
        port='55432',
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(CONST.get("_sql_title_2017").format(province=province))
    result_2017 = cur.fetchall()
    cur.execute(CONST.get("_sql_title_2021").format(province=province))
    result_2021 = cur.fetchall()
    conn.commit()
    totle_tile = list(set(
        [i.get("title") for i in result_2017] + 
        [i.get("title") for i in result_2021]
    ))
    _num = 1
    for title in totle_tile:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(CONST.get("_sql_mix").format(province=province, title=title))
        result = cur.fetchall()
        # cur.execute(CONST.get("_sql_insert_data").format(_id=_num, title=title, percentage=result[0].get("round")))
        # conn.commit()
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
    process_pool = ProcessPoolExecutor(max_workers=4)
    all_task = [process_pool.submit(main, (i.get("province"))) for i in result]
    wait(all_task, return_when=ALL_COMPLETED)
    process_pool.shutdown()
