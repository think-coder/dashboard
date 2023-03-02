# -*- coding:utf-8 -*-
import os
from concurrent.futures import ThreadPoolExecutor

import pyecharts.options as opts
from pyecharts.charts import Map

from database import pg, sql


class Dashboard(object):
    def __init__(self):
        self.map_data_path = "./map_data"

    def get_total_employer(self):
        conn = pg.get_connect()
        res = pg.execute_sql(conn, sql.GET_TOTAL_EMPLOYER)
        if not res:
            return {"total": 0}

        return {"total": res[0].get("count")}

    def get_employer_by_limit(self, page, num):
        conn = pg.get_connect()
        res = pg.execute_sql(conn, sql.GET_EMPLOYER_BY_LIMIT.format(limit=int(num), offset=int(page) * int(num)))
        employer_lst = [i.get("employer") for i in res]
        return {"employer_list": employer_lst}
    
    def get_employer(self, employer):
        conn = pg.get_connect()
        res = pg.execute_sql(conn, sql.GET_EMPLOYER.format(employer=employer))
        if not res:
            return {"employer": str()}

        return {"employer": res[0].get("employer")}

    def get_total_by_employer(self, employer):
        conn = pg.get_connect()
        res = pg.execute_sql(conn, sql.GET_TOTAL_BY_EMPLOYER.format(employer=employer))
        if not res:
            return {"total": 0}

        return {"total": res[0].get("count")}

    def get_employer_data_by_limit(self, employer, page, num):
        conn = pg.get_connect()
        res = pg.execute_sql(conn, sql.GET_EMPLOYER_DATA_BY_LIMIT.format(employer=employer, limit=int(num), offset=int(page) * int(num)))
        if not res:
            return {"data": list()}

        return {"data": res}

    def get_all_province(self):
        conn = pg.get_connect()
        res = pg.execute_sql(conn, sql.GET_ALL_PROVINCE)
        if not res:
            return {"data": list()}

        return {"data": [i.get("province") for i in res if i.get("province")]}
    
    def get_all_city(self, province):
        conn = pg.get_connect()
        res = pg.execute_sql(conn, sql.GET_ALL_CITY.format(province=province))
        if not res:
            return {"data": list()}
        
        return {"data": [i.get("city") for i in res if i.get("city")]}

    def get_city_by_province(self, province):
        conn = pg.get_connect()
        res = pg.execute_sql(conn, sql.GET_CITY_BY_PROVINCE.format(province=province))
        if not res:
            return {"data": list()}

        return {"data": [i.get("city") for i in res]}

    def get_map_by_country(self, country):
        save_path = "/".join([self.map_data_path, "country.html"])
        if os.path.exists(save_path):
            html_file = open(save_path, "r").read()
            return html_file

        province_data = self.compute_country_data(country)

        d_map = (
            Map()
            .add(
                series_name="每上市公司平均招聘数量",
                maptype="china",
                data_pair=province_data,
                is_selected=True,
                is_roam=True,
                center=None,
                name_map=None,
                symbol=None,
                is_map_symbol_show=True,
                layout_center=None,
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="全国各省级区域每上市公司平均招聘数量",
                    pos_left='30%',
                    pos_top='10'
                ),
                visualmap_opts=opts.VisualMapOpts(
                    min_=0,
                    max_=80,
                    range_text=["High", "Low"],
                    is_calculable=True,
                    is_piecewise=False,
                    # range_color=["white", "pink", "red"],
                    range_color=["#E0E0E0", "#CE0000"],
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                # itemstyle_opts=opts.ItemStyleOpts(color="transparent")
                showLegendSymbol=False
            )
            .render(path=save_path)
        )

        html_file = open(save_path, "r").read()
        return html_file

    def get_map_by_province(self, province):
        save_path = self.map_data_path + "/" + province + ".html"
        if os.path.exists(save_path):
            html_file = open(save_path, "r").read()
            return html_file
        
        city_data = self.compute_province_data(province)
        print(city_data)

        d_map = (
            Map()
            .add(
                series_name="{province}每上市公司平均招聘数量".format(province=province),
                maptype="广东",
                data_pair=city_data,
                is_selected=True,
                is_roam=True,
                center=None,
                name_map=None,
                symbol=None,
                is_map_symbol_show=True,
                layout_center=None,
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="{province}每上市公司平均招聘数量".format(province=province),
                    pos_left='30%',
                    pos_top='10'
                ),
                visualmap_opts=opts.VisualMapOpts(
                    min_=0,
                    max_=80,
                    range_text=["High", "Low"],
                    is_calculable=True,
                    is_piecewise=False,
                    # range_color=["white", "pink", "red"],
                    range_color=["#E0E0E0", "#CE0000"],
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                # itemstyle_opts=opts.ItemStyleOpts(color="transparent")
                showLegendSymbol=False
            )
            .render(path=save_path)
        )

        html_file = open(save_path, "r").read()
        return html_file

    def compute_country_data(self, country):
        province_data = list()
        # 获取省名称列表
        province_list = self.get_all_province().get("data", list())
        # 创建线程池，执行任务
        executor = ThreadPoolExecutor(max_workers=10)
        province_data = [data for data in executor.map(self.compute_country_province_data, province_list)]
        executor.shutdown()
        return province_data
    
    def compute_country_province_data(self, province):
        # 获取该省招聘总数
        _sql_1 = """SELECT COUNT(*) FROM dashboard_data WHERE work_province='{province}';""".format(province=province)
        conn = pg.get_connect()
        data = pg.execute_sql(conn, _sql_1)
        total_pos = data[0].get("count")
        # 获取该省招聘公司总数
        _sql_2 = """SELECT COUNT(DISTINCT(employer)) FROM dashboard_data WHERE work_province='{province}';""".format(province=province)
        conn = pg.get_connect()
        data = pg.execute_sql(conn, _sql_2)
        total_emp = data[0].get("count")
        # 计算每上市公司招聘数量
        # 区域每上市公司招聘数量 = 该区域内招聘需求总数 / 该区域内有招聘需求的上市公司总数
        per = round(total_pos / total_emp, 1) if total_emp else 0.0
        return [province, per]

    def compute_province_data(self, province):
        city_data = list()
        # 获取市名称列表
        city_list = self.get_all_city(province).get("data", list())
        # 创建线程池，执行任务
        executor = ThreadPoolExecutor(max_workers=10)
        city_data = [data for data in executor.map(self.compute_province_city_data, city_list)]
        executor.shutdown()
        return city_data
    
    def compute_province_city_data(self, city):
        # 获取该市招聘总数
        _sql_1 = """SELECT COUNT(*) FROM dashboard_data WHERE work_location='{worklocation}';""".format(worklocation=city)
        conn = pg.get_connect()
        data = pg.execute_sql(conn, _sql_1)
        total_pos = data[0].get("count")
        # 获取该省招聘公司总数
        _sql_2 = """SELECT COUNT(DISTINCT(employer)) FROM dashboard_data WHERE work_location='{worklocation}';""".format(worklocation=city)
        conn = pg.get_connect()
        data = pg.execute_sql(conn, _sql_2)
        total_emp = data[0].get("count")
        # 计算每上市公司招聘数量
        # 区域每上市公司招聘数量 = 该区域内招聘需求总数 / 该区域内有招聘需求的上市公司总数
        per = round(total_pos / total_emp, 1) if total_emp else 0.0
        print([city, per])
        return [city, per]
