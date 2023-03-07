import os
import pyecharts.options as opts
from pyecharts.charts import Map
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Data, ProvinceCityMap


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def compute_province_per(country):
    """计算国级平均招聘量"""
    data_list = ProvinceCityMap.objects.all().distinct("province")
    per_list = list()
    for data in data_list:
        province = data.province
        pos_count = Data.objects.filter(work_province=province).count()
        employer_count = Data.objects.filter(work_province=province).distinct("employer").count()
        per = round(pos_count / employer_count, 1)
        per_list.append([province, per])
    return per_list

def compute_city_per(province):
    """计算省级平均招聘量"""
    data_list = ProvinceCityMap.objects.filter(province=province).distinct("city")
    per_list = list()
    for data in data_list:
        city = data.city
        pos_count = Data.objects.filter(work_province=province).filter(work_location=city).count()
        employer_count = Data.objects.filter(work_province=province).filter(work_location=city).distinct("employer").count()
        per = round(pos_count / employer_count, 1)
        per_list.append([city, per])
    return per_list

def get_employer(request, employer):
    """检索雇主是否存在"""
    data = Data.objects.filter(employer__icontains = employer).distinct("employer")
    employer_list = [i.employer for i in data]

    return JsonResponse({
        "data": employer_list
    })

def get_total_employer(request):
    """获取雇主总数"""
    data = Data.objects.all().distinct("employer").count()
    return JsonResponse({
        "data": data
    })

def get_employer_by_limit(request, page, num):
    """获取区间雇主列表"""
    data = Data.objects.all().distinct("employer")[int(page)*(int(num)-1):int(page)*int(num)+int(num)]
    employer_list = [i.employer for i in data]
    return JsonResponse({
        "data": employer_list
    })

def get_total_by_employer(request, employer):
    """根据雇主名称获取招聘数量"""
    data = Data.objects.filter(employer=employer).count()
    return JsonResponse({
        "data": data
    })

def get_employer_data_by_limit(request, employer, page, num):
    """获取雇主的区间数据"""
    data = Data.objects.filter(employer=employer)[int(page)*(int(num)-1):int(page)*int(num)+int(num)]
    employer_list = [i.employer for i in data]
    return JsonResponse({
        "data": employer_list
    })

def get_all_province(request):
    """获取所有省份名称"""
    res_data = ProvinceCityMap.objects.all().distinct("province")
    province_list = [i.province for i in res_data]
    print(province_list)
    return JsonResponse({
        "data": province_list
    })

def get_city_by_province(request, province):
    """获取省份下属市县名称"""
    res_data = ProvinceCityMap.objects.filter(province=province)
    city_list = [i.city for i in res_data]
    print(city_list)
    return JsonResponse({
        "data": city_list
    })

def get_map_by_country(request, country):
    """获取国级展示图"""
    file_name = ".".join([country, "html"])
    save_path = "./dashboard/templates/"
    if os.path.exists(save_path + file_name):
        return render(request, file_name, {})
    per_list = compute_province_per(country)

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
            .render(path=save_path + file_name)
        )    

    return render(request, file_name, {})

def get_map_by_province(request, province):
    """获取省级展示图"""
    file_name = ".".join([province, "html"])
    save_path = "./dashboard/templates/"
    if os.path.exists(save_path + file_name):
        return render(request, file_name, {})

    per_list = compute_city_per(province)
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
    province_maptype = province_maptype.get(province, province)
    d_map = (
            Map()
            .add(
                series_name="每上市公司平均招聘数量",
                maptype=province_maptype,
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
            .render(path=save_path + file_name)
        )    

    return render(request, file_name, {})



def load_data(request):
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

