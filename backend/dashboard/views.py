import os
import pyecharts.options as opts
from pyecharts.charts import Map, Timeline
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Data, ProvinceCityMap, ProvinceMaptype


import time
import json
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED

# # 实例化调度器
# scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
# # 调度器使用DjangoJobStore()
# scheduler.add_jobstore(DjangoJobStore(), "default")

# @register_job(scheduler, "interval", seconds=600, args=[''], id='job_generate_country_map', replace_existing=True)
# def job_generate_country_map(param):
#     """任务: 生成国级HTML文件"""
#     print("Begin: job_generate_country_map")
#     Logic().generate_country_map("中国")
#     print("End: job_generate_country_map")

# @register_job(scheduler, "interval", seconds=600, args=[''], id='job_generate_province_map', replace_existing=True)
# def job_generate_province_map(param):
#     """任务: 生成省级HTML文件"""
#     print("Begin: job_generate_province_map")
#     res_data = ProvinceCityMap.objects.all().distinct("province")
#     province_list = [i.province for i in res_data]
    
#     # 构建线程池，批处理任务
#     pool = ThreadPoolExecutor(max_workers=10)
#     all_task=[pool.submit(Logic().generate_province_map, (i)) for i in province_list]
#     wait(all_task, return_when=ALL_COMPLETED)
#     pool.shutdown()
#     print("End: job_generate_province_map")

# register_events(scheduler)
# scheduler.start()


class Compute(object):
    def compute_province_per(self, country, year):
        """计算国级平均招聘量"""
        data_list = ProvinceCityMap.objects.all().distinct("province")
        per_list = [["", 0]]
        for data in data_list:
            province = data.province
            pos_count = Data.objects.filter(year=year).filter(work_province=province).count()
            employer_count = Data.objects.filter(year=year).filter(work_province=province).distinct("employer").count()
            if not pos_count or not employer_count:
                return per_list
            per = round(pos_count / employer_count, 1)
            per_list.append([province, per])
        return per_list

    def compute_city_per(self, province, year):
        """计算省级平均招聘量"""
        data_list = ProvinceCityMap.objects.filter(province__icontains=province).distinct("city")
        per_list = [["", 0]]
        for data in data_list:
            city = data.city
            pos_count = Data.objects.filter(year=year).filter(work_province__icontains=province).filter(work_location=city).count()
            employer_count = Data.objects.filter(year=year).filter(work_province__icontains=province).filter(work_location=city).distinct("employer").count()
            if not pos_count or not employer_count:
                return per_list
            per = round(pos_count / employer_count, 1)
            per_list.append([city, per])
        return per_list


class Logic(object):
    def __init__(self):
        self.file_name = "{file_name}.html"
        self.save_path = "./dashboard/templates/"

    def get_employer(self, request, employer):
        """检索雇主是否存在"""
        data = Data.objects.filter(employer__icontains = employer).distinct("employer")
        employer_list = [i.employer for i in data]

        return JsonResponse({
            "data": employer_list
        })

    def get_total_employer(self, request):
        """获取雇主总数"""
        data = Data.objects.all().distinct("employer").count()

        return JsonResponse({
            "data": data
        })

    def get_employer_by_limit(self, request, page, num):
        """获取区间雇主列表"""
        data = Data.objects.all().distinct("employer")[int(page)*(int(num)-1):int(page)*int(num)+int(num)]
        employer_list = [i.employer for i in data]

        return JsonResponse({
            "data": employer_list
        })

    def get_total_by_employer(self, request, employer):
        """根据雇主名称获取招聘数量"""
        data = Data.objects.filter(employer=employer).count()

        return JsonResponse({
            "data": data
        })

    def get_employer_data_by_limit(self, request, employer, page, num):
        """获取雇主的区间数据"""
        data = Data.objects.filter(employer=employer)[int(page)*(int(num)-1):int(page)*int(num)+int(num)]
        employer_list = [i.employer for i in data]

        return JsonResponse({
            "data": employer_list
        })

    def get_all_province(self, request):
        """获取所有省份名称"""
        res_data = ProvinceCityMap.objects.all().distinct("province")
        province_list = [i.province for i in res_data]

        return JsonResponse({
            "data": province_list
        })

    def get_city_by_province(self, request, province):
        """获取省份下属市县名称"""
        res_data = ProvinceCityMap.objects.filter(province=province)
        city_list = [i.city for i in res_data]

        return JsonResponse({
            "data": city_list
        })

    def get_map_by_country(self, request, country):
        """获取国级展示图"""
        if os.path.exists(self.save_path + self.file_name.format(file_name=country)):
            return render(request, self.file_name.format(file_name=country), {})
        
        self.generate_country_map(country)

        return render(request, self.file_name.format(file_name=country), {})

    def get_map_by_province(self, request, province):
        """获取省级展示图"""
        if os.path.exists(self.save_path + self.file_name.format(file_name=province)):
            return render(request, self.file_name.format(file_name=province), {})

        self.generate_province_map(province)

        return render(request, self.file_name.format(file_name=province), {})

    def generate_country_map(self, country):
        """生成国级HTML文件"""
        print("### Country: {} ###".format(country))
        year_list = [i.year for i in Data.objects.all().distinct("year")]
        print("### Yearlist: {} ###".format(year_list))
        time_line = Timeline()
        for year in year_list:
            print("### Year: {} ###".format(year))
            per_list = Compute().compute_province_per(country, year)
            d_map = (
                Map()
                .add(
                    series_name="每上市公司平均招聘数量",
                    maptype="china",
                    data_pair=per_list,

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
            )
            time_line.add(d_map, year)
        time_line.add_schema(is_auto_play=False, play_interval=1000)
        time_line.render(self.save_path + self.file_name.format(file_name=country))

    def generate_province_map(self, province):
        """生成省级HTML文件"""
        print("### Province: {}###".format(province))
        year_list = [i.year for i in Data.objects.all().distinct("year")]
        print("### Yearlist: {} ###".format(year_list))
        time_line = Timeline()
        for year in year_list:
            print("### Year: {} ###".format(year))
            per_list = Compute().compute_city_per(province, year)
            data_maptype = ProvinceMaptype.objects.filter(province=province)
            maptype = str()
            if not data_maptype or len(data_maptype) != 1:
                maptype = province
            else:
                maptype = data_maptype[0].maptype

            d_map = (
                Map()
                .add(
                    series_name="每上市公司平均招聘数量",
                    maptype=maptype,
                    data_pair=per_list,
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
                # .render(path=save_path + file_name)
            )    
            time_line.add(d_map, year)

        time_line.add_schema(is_auto_play=False, play_interval=1000)
        time_line.render(self.save_path + self.file_name.format(file_name=province))

    def tool_load_data(self, request):
        """暂用：导入数据"""
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(
            database='dashboard',
            user='postgres',
            password='postgres',
            host='106.52.123.19',
            port='5432',
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        for i in range(1, 4193545):
            print("第{_num}条数据...".format(_num=i))
            _sql = """
                SELECT * FROM data WHERE id={_id};
            """
            cur.execute(_sql.format(_id=i))
            result = cur.fetchall()
            conn.commit()
            for res in result:
                _id=res.get("id")
                _ticker=res.get("ticker")
                _employer=res.get("employer")
                _title=res.get("title")
                _salary_range=res.get("salary_range")
                _a_sala_range_start=res.get("a_sala_range_start")
                _a_sala_range_end=res.get("a_sala_range_end")
                _work_experience=res.get("work_experience")
                _work_location=res.get("work_location")
                _edu_require=res.get("edu_require")
                _publish_date=res.get("publish_date")
                _source=res.get("source")
                _pos_require=res.get("pos_require")
                _lang_require=res.get("lang_require")
                _age_require=res.get("age_require")
                _employ_type=res.get("employ_type")
                _year=res.get("year")
                _day=res.get("day")
                _count=res.get("count")
                _industry=res.get("industry")
                _work_province=res.get("work_province")
                if not _id:
                    _id = 0
                if not _ticker:
                    _ticker = 0
                if not _employer:
                    _employer = "None"
                if not _title:
                    _title = "None"
                if not _salary_range:
                    _salary_range = "None"
                if not _a_sala_range_start:
                    _a_sala_range_start = 0
                if not _a_sala_range_end:
                    _a_sala_range_end = 0
                if not _work_experience:
                    _work_experience = "None"
                if not _work_location:
                    _work_location = "None"
                if not _edu_require:
                    _edu_require = "None"
                if not _publish_date:
                    _publish_date = "None"
                if not _source:
                    _source = "None"
                if not _pos_require:
                    _pos_require = "None"
                if not _lang_require:
                    _lang_require = "None"
                if not _age_require:
                    _age_require = "None"
                if not _employ_type:
                    _employ_type = "None"
                if not _year:
                    _year = 0
                if not _day:
                    _day = 0
                if not _count:
                    _count = 0
                if not _industry:
                    _industry = "None"
                if not _work_province:
                    _work_province = "None"
                
                Data.objects.create(
                    id=_id,
                    ticker=_ticker,
                    employer=_employer,
                    title=_title,
                    salary_range=_salary_range,
                    a_sala_range_start=_a_sala_range_start,
                    a_sala_range_end=_a_sala_range_end,
                    work_experience=_work_experience,
                    work_location=_work_location,
                    edu_require=_edu_require,
                    publish_date=_publish_date,
                    source=_source,
                    pos_require=_pos_require,
                    lang_require=_lang_require,
                    age_require=_age_require,
                    employ_type=_employ_type,
                    year=_year,
                    day=_day,
                    count=_count,
                    industry=_industry,
                    work_province=_work_province
                )

        cur.close()
        conn.close()

        return HttpResponse("Finish")

    def tool_generate_country_map(self, request):
        """任务: 生成国级HTML文件"""
        print("Begin: job_generate_country_map")
        self.generate_country_map("中国")
        print("End: job_generate_country_map")

        return JsonResponse({
            "data": "OK"
        })

    def tool_generate_province_map(self, request):
        """任务: 生成省级HTML文件"""
        print("Begin: job_generate_province_map")
        res_data = ProvinceCityMap.objects.all().distinct("province")
        province_list = [i.province for i in res_data]
        
        # 构建线程池，批处理任务
        pool = ThreadPoolExecutor(max_workers=10)
        all_task=[pool.submit(self.generate_province_map, (i)) for i in province_list]
        wait(all_task, return_when=ALL_COMPLETED)
        pool.shutdown()
        print("End: job_generate_province_map")

        return JsonResponse({
            "data": "OK"
        })
