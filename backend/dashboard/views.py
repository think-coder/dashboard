from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Data, ProvinceCityMap


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get_employer(request, employer):
    """检索雇主是否存在"""
    data = Data.objects.filter(employer=employer).distinct("employer")
    if not data or len(data) != 1:
        return HttpResponse(str())

    for i in data:
        return HttpResponse(i.employer)

def get_total_employer(request):
    """获取雇主总数"""
    total_count = Data.objects.count()
    return HttpResponse(total_count)

def get_employer_by_limit(request, page, num):
    """获取区间雇主列表"""
    employer_list = Data.objects.all().distinct("employer")[int(page)*(int(num)-1):int(page)*int(num)+int(num)]
    print(employer_list)
    print(type(employer_list))
    return HttpResponse(employer_list)

def get_total_by_employer(request, employer):
    """根据雇主名称获取招聘数量"""
    employer_count = Data.objects.filter(employer=employer).count()
    print(employer_count)
    return HttpResponse(employer_count)

def get_employer_data_by_limit(request, employer, page, num):
    """获取雇主的区间数据"""
    employer_list = Data.objects.filter(employer=employer)[int(page)*(int(num)-1):int(page)*int(num)+int(num)]
    print(employer_list)
    return HttpResponse(employer_list)

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
    print(country)
    return render(request, "country.html", {})

def get_map_by_province(request, province):
    """获取省级展示图"""
    print(province)
    return render(request, "country.html", {})

def load_data(request):
    import psycopg2
    import psycopg2.extras
    conn = psycopg2.connect(
        database='dashboard',
        user='postgres',
        password='postgres',
        host='127.0.0.1',
        port='5432',
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    for i in range(1, 4193544):
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

