import os
import time

import gvcode
import pyecharts.options as opts
from pyecharts.charts import Map, Bar, Timeline
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.utils.decorators import method_decorator

from dashboard import models


total_dict = {}

class Compute(object):
    def __init__(self):
        self.province_obj_map = {
            "新疆维吾尔自治区": models.XinJiang.objects.all(),
            "青海省": models.QingHai.objects.all(),
            "湖北省": models.HuBei.objects.all(),
            "山西省": models.ShanXi_1.objects.all(),
            "云南省": models.YunNan.objects.all(),
            "河北省": models.HeBei.objects.all(),
            "广西壮族自治区": models.GuangXi.objects.all(),
            "海南省": models.HaiNan.objects.all(),
            "上海市": models.ShangHai.objects.all(),
            "辽宁省": models.LiaoNing.objects.all(),
            "福建省": models.FuJian.objects.all(),
            "陕西省": models.ShanXi_2.objects.all(),
            "四川省": models.SiChuan.objects.all(),
            "贵州省": models.GuiZhou.objects.all(),
            "广东省": models.GuangDong.objects.all(),
            "北京市": models.BeiJing.objects.all(),
            "黑龙江省": models.HeiLongJiang.objects.all(),
            "江苏省": models.JiangSu.objects.all(),
            "天津市": models.TianJin.objects.all(),
            "重庆市": models.ChongQing.objects.all(),
            "山东省": models.ShanDong.objects.all(),
            "内蒙古自治区": models.NeiMengGu.objects.all(),
            "宁夏回族自治区": models.NingXia.objects.all(),
            "浙江省": models.ZheJiang.objects.all(),
            "西藏自治区": models.XiZang.objects.all(),
            "吉林省": models.JiLin.objects.all(),
            "安徽省": models.AnHui.objects.all(),
            "江西省": models.JiangXi.objects.all(),
            "甘肃省": models.GanSu.objects.all(),
            "河南省": models.HeNan.objects.all(),
            "湖南省": models.HuNan.objects.all(),
        }
        self.year_obj_map = {
            "2017": models.Year2017.objects.all(),
            "2018": models.Year2018.objects.all(),
            "2019": models.Year2019.objects.all(),
            "2020": models.Year2020.objects.all(),
            "2021": models.Year2021.objects.all(),
            "2022": models.Year2022.objects.all(),
        }

    def compute_province_per(self, country, year):
        """计算国级平均招聘量"""
        data_list = models.ProvinceCityMap.objects.all().distinct("province")
        per_list = [["", 0]]
        year_data = self.year_obj_map.get(year)
        for data in data_list:
            province = data.province
            pos_count = year_data.filter(work_province=province).count()
            employer_count = year_data.filter(work_province=province).distinct("employer").count()
            if not pos_count or not employer_count:
                return per_list
            per = round(pos_count / employer_count, 1)
            per_list.append([province, per])
            # 更新数据库(有则更新，无则创建)
            province_data = models.PercentageData.objects.all().filter(year=year).filter(country=country).filter(province=province).filter(city="ALL").first()
            if not province_data:
                models.PercentageData.objects.create(
                    country=country,
                    province=province,
                    city="ALL",
                    year=year,
                    percentage=per
                )
                continue
            province_data.country = country
            province_data.province = province
            province_data.city = "ALL"
            province_data.year = year
            province_data.percentage = per
        return per_list

    def compute_city_per(self, province, year):
        """计算省级平均招聘量"""
        data_list = models.ProvinceCityMap.objects.filter(province__icontains=province).distinct("city")
        per_list = [["", 0]]
        province_data = self.province_obj_map.get(province)
        for data in data_list:
            city = data.city
            pos_count = province_data.filter(year=year).filter(work_location=city).count()
            employer_count = province_data.filter(year=year).filter(work_location=city).distinct("employer").count()
            if not pos_count or not employer_count:
                return per_list
            per = round(pos_count / employer_count, 1)
            per_list.append([city, per])
            # 更新数据库(有则更新，无则创建)
            city_data = models.PercentageData.objects.all().filter(year=year).filter(country="中国").filter(province=province).filter(city=city).first()
            if not city_data:
                models.PercentageData.objects.create(
                    country="中国",
                    province=province,
                    city=city,
                    year=year,
                    percentage=per
                )
                continue
            province_data.country = "中国"
            province_data.province = province
            province_data.city = city
            province_data.year = year
            province_data.percentage = per
        return per_list

    def compute_rise_per(self, title):
        """计算增长率"""
        left_point = self.year_obj_map.get("2017").filter(title=title).count()
        right_point = self.year_obj_map.get("2021").filter(title=title).count()
        if not left_point or not right_point:
            per = round(right_point ** 1/4 - 1, 1)
        else:
            per = round((right_point / left_point) ** 1/4 - 1, 1)
        models.PercentageTitle.objects.update_or_create(
            title=title,
            percentage=per
        )
        return (per, title)


class Logic(object):
    def __init__(self):
        self.file_name = "{file_name}.html"
        self.save_path = "./dashboard/templates/"
        self.checkcode_img_path = "./dashboard/checkcode-img/{text}.jpg"
        self.year_obj_map = {
            "2017": models.Year2017.objects.all(),
            "2018": models.Year2018.objects.all(),
            "2019": models.Year2019.objects.all(),
            "2020": models.Year2020.objects.all(),
            "2021": models.Year2021.objects.all(),
            "2022": models.Year2022.objects.all(),
        }
        self.top_city_list = [
            "北京市", "上海市", "广州市", "深圳市",
            "成都市", "重庆市", "杭州市", "西安市", "武汉市",
            "苏州市", "郑州市", "南京市", "天津市", "长沙市",
            "东莞市", "宁波市", "佛山市", "合肥市", "青岛市"
        ]

    def login(self, request):
        """用户登录"""
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            checkcode = request.POST.get("checkcode")
            code_uuid = request.POST.get("uuid")
            if checkcode.lower() != total_dict[str(code_uuid)].lower():
                total_dict.clear()
                return JsonResponse({
                    "code": 404,
                    "data": "验证码错误"
                })
            
            total_dict.clear()
            user = authenticate(username=username,password=password)
            if not user:
                return JsonResponse({
                    "code": 404,
                    "data": "用户名或密码错误"
                })
            else:
                login(request, user)
                res = JsonResponse({
                    "code": 200,
                    "data": "登录成功"
                })
                res['Access-Control-Expose-Headers'] = "*"
                res['Access-Control-Allow-Origin'] = "*"
                return res
        else:
            return JsonResponse({
                "code": 500,
                "data": "服务端异常"
            })

    def logout(self, request):
        """用户登出"""
        logout(request)
        return JsonResponse({
            "code": 200,
            "data": "登出成功"
        })

    def registry(self, request):
        """用户注册"""
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            if not User.objects.filter(username=username):
                user = User.objects.create_user(username=username, password=password)
                return JsonResponse({
                    "code": 200,
                    "data": "注册成功"
                })
            else:
                return JsonResponse({
                    "code": 404,
                    "data": "用户名已存在"
                })
        else:
            return JsonResponse({
                "code": 500,
                "data": "服务端异常"
            })

    def get_image_code(self, request, code_uuid):
        """获取验证码图片"""
        image, text = gvcode.generate()
        image.save(self.checkcode_img_path.format(text=text))
        total_dict[str(code_uuid)] = text
        with open(self.checkcode_img_path.format(text=text), 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type='image/jpg')

    # @method_decorator(login_required())
    def get_employer(self, request, employer):
        """检索雇主是否存在"""
        data = models.Employer.objects.filter(name__icontains = employer)
        employer_list = [i.name for i in data]

        return JsonResponse({
            "data": employer_list
        })

    # @method_decorator(login_required())
    def get_total_employer(self, request):
        """获取雇主总数"""
        data = models.Employer.objects.all().distinct("name").count()

        return JsonResponse({
            "data": data
        })

    # @method_decorator(login_required())
    def get_employer_by_limit(self, request, page, num):
        """获取区间雇主列表"""
        data = models.Employer.objects.all()
        data_total = data.distinct("name").count()
        data_employer = data[int(page)*(int(num)-1):int(page)*int(num)+int(num)]
        employer_list = [i.name for i in data_employer]

        return JsonResponse({
            "total": data_total,
            "data": employer_list
        })

    # @method_decorator(login_required())
    def get_total_by_employer(self, request, employer):
        """根据雇主名称获取招聘数量"""
        data = models.Data.objects.filter(employer=employer).count()

        return JsonResponse({
            "data": data
        })

    # @method_decorator(login_required())
    def get_employer_data_by_limit(self, request, employer, page, num):
        """获取雇主的区间数据"""
        data = models.Data.objects.filter(employer=employer)
        data_total = data.count()
        data_employer = data[(int(page) - 1) * int(num): int(page)*int(num)]

        employer_list = list()
        for i in data_employer:
            employer_list.append({
                "股票代码": i.ticker,
                "雇主名称": i.employer,
                "职位名称": i.title,
                "薪资范围": i.salary_range,
                "年薪下限": i.a_sala_range_start,
                "年薪上限": i.a_sala_range_end,
                "工作经验要求": i.work_experience,
                "工作地点": i.work_location,
                "学历要求": i.edu_require,
                "发布日期": i.publish_date,
                "语言要求": i.lang_require,
                "年龄要求": i.age_require,
                "雇主所在行业": i.industry,
                "pos_require": i.pos_require,
                "pos_text": i.pos_require
            })

        return JsonResponse({
            "total": data_total,
            "data": employer_list
        })

    # @method_decorator(login_required())
    def get_all_country(self, request):
        """获取所有国家名称"""
        province_list = ["中国"]

        return JsonResponse({
            "data": province_list
        })

    # @method_decorator(login_required())
    def get_all_province(self, request):
        """获取所有省份名称"""
        res_data = models.ProvinceCityMap.objects.all().distinct("province")
        province_list = [i.province for i in res_data]

        return JsonResponse({
            "data": province_list
        })

    # @method_decorator(login_required())
    def get_city_by_province(self, request, province):
        """获取省份下属市县名称"""
        res_data = models.ProvinceCityMap.objects.filter(province=province)
        city_list = [i.city for i in res_data]

        return JsonResponse({
            "data": city_list
        })

    # @method_decorator(login_required())
    def get_map_by_country(self, request, country):
        """获取国级展示图"""
        if os.path.exists(self.save_path + self.file_name.format(file_name=country)):
            return render(request, self.file_name.format(file_name=country), {})
        
        self.generate_country_map(country)

        return render(request, self.file_name.format(file_name=country), {})
    
    # @method_decorator(login_required())
    def get_data_by_country(self, request, country):
        """获取国级展示图-数据"""
        data_list = list()
        year_list = [data.year for data in models.YearList.objects.all().distinct("year")]
        for year in year_list:
            data_dict = dict()
            data_dict["时间"] = year
            for item in models.ProvinceCityMap.objects.all().distinct("province"):
                data_dict[item.province] = "None"
                province_data = models.PercentageData.objects.all().filter(year=year).filter(country=country).filter(city="ALL")
                for province in province_data:
                    if item.province == province.province:
                        data_dict[item.province] = province.percentage
            data_list.append(data_dict)

        return JsonResponse({
            "code": 200,
            "data": data_list
        })

    # @method_decorator(login_required())
    def get_map_by_province(self, request, province):
        """获取省级展示图"""
        if os.path.exists(self.save_path + self.file_name.format(file_name=province)):
            return render(request, self.file_name.format(file_name=province), {})

        self.generate_province_map(province)

        return render(request, self.file_name.format(file_name=province), {})
    
    # @method_decorator(login_required())
    def get_data_by_province(self, request, province):
        """获取省级展示图-数据"""
        data_list = list()
        year_list = [data.year for data in models.YearList.objects.all().distinct("year")]
        for year in year_list:
            data_dict = dict()
            data_dict["时间"] = year
            for item in models.ProvinceCityMap.objects.filter(province=province):
                data_dict[item.city] = "None"
                city_data = models.PercentageData.objects.all().filter(year=year).filter(country="中国").filter(province=province)
                for city in city_data:
                    if city.city == "ALL":
                        continue
                    if item.city == city.city:
                        data_dict[item.city] = city.percentage
            data_list.append(data_dict)
        
        return JsonResponse({
            "code": 200,
            "data": data_list
        })

    # @method_decorator(login_required())
    def get_map_of_top_city(self, request):
        """获取一线/新一线HTML图"""
        if os.path.exists(self.save_path + self.file_name.format(file_name="新一线")):
            return render(request, self.file_name.format(file_name="新一线"), {})

        self.generate_map_of_top_city()

        return render(request, self.file_name.format(file_name="新一线"), {})
    
    # @method_decorator(login_required())
    def get_data_of_top_city(self, request):
        """获取一线/新一线HTML图-数据"""
        data_list = list()
        year_list = [data.year for data in models.YearList.objects.all().distinct("year")]
        for year in year_list:
            data_dict = dict()
            data_dict["时间"] = year
            for city in self.top_city_list:
                data_dict[city] = "None"
                city_data = models.PercentageData.objects.all().filter(year=year).filter(country="中国").filter(city=city).first()
                if city_data:
                    data_dict[city] = city_data.percentage
            data_list.append(data_dict)
        
        return JsonResponse({
            "code": 200,
            "data": data_list
        })

    # @method_decorator(login_required())
    def get_map_of_top_rise(self, request):
        """获取需求增加最快的15种岗位"""
        if os.path.exists(self.save_path + self.file_name.format(file_name="增长最快")):
            return render(request, self.file_name.format(file_name="增长最快"), {})

        self.generate_map_of_top_rise()

        return render(request, self.file_name.format(file_name="增长最快"), {})
    
    # @method_decorator(login_required())
    def get_data_of_top_rise(self, request):
        """获取需求增加最快的15种岗位-数据"""
        pass

    # @method_decorator(login_required())
    def get_map_of_tail_reduce(self, request):
        """获取需求下降最快的15种岗位"""
        if os.path.exists(self.save_path + self.file_name.format(file_name="下降最快")):
            return render(request, self.file_name.format(file_name="下降最快"), {})

        self.generate_map_of_tail_reduce()

        return render(request, self.file_name.format(file_name="下降最快"), {})
    
    # @method_decorator(login_required())
    def get_data_of_tail_reduce(self, request):
        """获取需求下降最快的15种岗位-数据"""
        pass

    def generate_country_map(self, country):
        """生成国级HTML文件"""
        print("### Country: {} ###".format(country))
        year_list = [data.year for data in models.YearList.objects.all().distinct("year")]
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
        year_list = [data.year for data in models.YearList.objects.all().distinct("year")]
        print("### Yearlist: {} ###".format(year_list))
        time_line = Timeline()
        for year in year_list:
            print("### Year: {} ###".format(year))
            per_list = Compute().compute_city_per(province, year)
            data_maptype = models.ProvinceMaptype.objects.filter(province=province)
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

    def generate_map_of_top_city(self):
        """生成一线/新一线HTML文件"""
        print("### Top cipy: {}###".format("新一线"))
        year_list = [data.year for data in models.YearList.objects.all().distinct("year")]
        print("### Yearlist: {} ###".format(year_list))

        time_line = Timeline()
        for year in year_list:
            per_list = []
            for city in self.top_city_list:
                print("city: {}".format(city))
                city_year_data = models.Data.objects.filter(work_location=city).filter(year=year)
                pos_count = city_year_data.count()
                employer_count = city_year_data.distinct("employer").count()
                if not pos_count or not employer_count:
                    per_list.append(0)
                    continue
                per_list.append(round(pos_count / employer_count, 1))
            print("per_list: {}".format(per_list))

            d_bar = (
                Bar()
                .add_xaxis(self.top_city_list)
                .add_yaxis("每上市公司平均招聘量", per_list)
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="一线/新一线城市每上市公司平均招聘量", subtitle=""),
                    xaxis_opts=opts.AxisOpts(name="城市名称"),
                    yaxis_opts=opts.AxisOpts(name="每上市公司平均招聘量")
                )
                # .render(self.save_path + self.file_name.format(file_name="新一线"))
            )
            time_line.add(d_bar, year)
        time_line.add_schema(is_auto_play=False, play_interval=1000)
        time_line.render(self.save_path + self.file_name.format(file_name="新一线"))

    def generate_map_of_top_rise(self):
        """生成需求增加最快的15种岗位"""
        top_per_data = models.PercentageTitle.objects.all().order_by("-percentage")[15:]
        top_per_list = list()
        top_title_list = list()
        for i in top_per_data:
            top_per_list.append(i.percentage)
            top_title_list.append(i.title)
        top_per_list = top_per_list[::-1]
        top_title_list = top_title_list[::-1]
        d_bar = (
            Bar()
            .add_xaxis(top_title_list)
            .add_yaxis("每上市公司平均招聘量", top_per_list)
            .reversal_axis()
            .set_global_opts(
                title_opts=opts.TitleOpts(title="2017-2021需求复合增长率(%)", subtitle=""),
                xaxis_opts=opts.AxisOpts(name="职位"),
                yaxis_opts=opts.AxisOpts(name="增长率")
            )
            .render(self.save_path + self.file_name.format(file_name="增长最快"))
        )
        print("End generate_map_of_top_rise")

    def generate_map_of_tail_reduce(self):
        """生成需求下降最快的15种岗位"""
        top_per_data = models.PercentageTitle.objects.all().order_by("percentage")[0:15]
        top_per_list = list()
        top_title_list = list()
        for i in top_per_data:
            top_per_list.append(i.percentage)
            top_title_list.append(i.title)
        d_bar = (
            Bar()
            .add_xaxis(top_title_list)
            .add_yaxis("每上市公司平均招聘量", top_per_list)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="2017-2021需求复合增长率(%)", subtitle=""),
                xaxis_opts=opts.AxisOpts(name="职位"),
                yaxis_opts=opts.AxisOpts(name="增长率")
            )
            .render(self.save_path + self.file_name.format(file_name="下降最快"))
        )
        print("End generate_map_of_tail_reduce")

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
                
                models.Data.objects.create(
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

    def job_generate_country_map(self, request):
        """任务: 生成国级HTML文件"""
        print("Begin: job_generate_country_map")
        self.generate_country_map("中国")
        print("End: job_generate_country_map")

        return JsonResponse({
            "data": "OK"
        })

    def job_generate_province_map(self, request):
        """任务: 生成省级HTML文件"""
        print("Begin: job_generate_province_map")
        res_data = models.ProvinceCityMap.objects.all().distinct("province")
        province_list = [i.province for i in res_data]
        print(len(province_list), province_list)
        
        # 构建线程池，批处理任务
        pool = ThreadPoolExecutor(max_workers=10)
        all_task=[pool.submit(self.generate_province_map, (i)) for i in province_list]
        wait(all_task, return_when=ALL_COMPLETED)
        pool.shutdown()
        print("End: job_generate_province_map")

        return JsonResponse({
            "data": "OK"
        })

    def job_generate_columnar_map(self, request):
        """任务: 生成一线/新一线HTML文件"""
        print("Begin: job_generate_columnar_map")
        self.generate_map_of_top_city()
        print("End: job_generate_columnar_map")

        return JsonResponse({
            "data": "OK"
        }) 

    def job_generate_map_of_rise_reduce(self, request):
        """任务: 生成需求增加/下降最快的15种岗位"""
        _start = time.time()
        print("Begin: job_generate_map_of_rise_reduce")
        title_list = [i.title for i in models.Data.objects.distinct("title")]
        total_title = len(title_list)
        per_list = list()
        map_dict = dict()

        _num = 1
        executor = ThreadPoolExecutor(max_workers=8)
        for per, title in executor.map(Compute().compute_rise_per, title_list):
            per_list.append(per)
            map_dict[str(per)] = title
            print(_num, "/", total_title, title, per)
            _num += 1

        # per_list.sort()
        # top_per_list = per_list[0:15]
        # tail_per_list = per_list[-15:]
        # top_list = [map_dict.get(str(per)) for per in top_per_list]
        # tail_list = [map_dict.get(str(per)) for per in tail_per_list]
        # rise_bar = (
        #     Bar()
        #     .add_xaxis(top_list)
        #     .add_yaxis("每上市公司平均招聘量", top_per_list)
        #     .set_global_opts(
        #         title_opts=opts.TitleOpts(title="需求增长最快的15种岗位", subtitle=""),
        #         xaxis_opts=opts.AxisOpts(name="职位"),
        #         yaxis_opts=opts.AxisOpts(name="增长率")
        #     )
        #     .render(self.save_path + self.file_name.format(file_name="增长最快"))
        # )
        # reduce_bar = (
        #     Bar()
        #     .add_xaxis(tail_list)
        #     .add_yaxis("每上市公司平均招聘量", tail_per_list)
        #     .set_global_opts(
        #         title_opts=opts.TitleOpts(title="需求下降最快的15种岗位", subtitle=""),
        #         xaxis_opts=opts.AxisOpts(name="职位"),
        #         yaxis_opts=opts.AxisOpts(name="增长率")
        #     )
        #     .render(self.save_path + self.file_name.format(file_name="下降最快"))
        # )
        # _end = time.time()
        # print("End: job_generate_map_of_rise_reduce")
        # print("Total: {}".format(_end - _start))

        return JsonResponse({
            "data": "OK"
        })

    def tool_load_data_by_year(self, request):
        year_list = [data.year for data in models.YearList.objects.all().distinct("year")]
        for year in year_list:
            print(year)
            all_data = models.Data.objects.all().filter(year=year)
            for data in all_data:
                if year == 2017:
                    models.Year2017.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )
                elif year == 2018:
                    models.Year2018.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

                elif year == 2019:
                    models.Year2019.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

                elif year == 2020:
                    models.Year2020.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

                elif year == 2021:
                    models.Year2021.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

                elif year == 2022:
                    models.Year2022.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

        return JsonResponse({
            "data": "OK"
        }) 

    def tool_load_data_by_province(self, request):
        province_list = models.Data.objects.all().distinct("work_province")

        for province in province_list:
            print(province.work_province)
            if province.work_province == "北京市":
                data_list = models.Data.objects.all().filter(work_province="北京市")
                for data in data_list:
                    models.BeiJing.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "上海市":
                data_list = models.Data.objects.all().filter(work_province="上海市")
                for data in data_list:
                    models.ShangHai.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "云南省":
                data_list = models.Data.objects.all().filter(work_province="云南省")
                for data in data_list:
                    models.YunNan.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "内蒙古自治区":
                data_list = models.Data.objects.all().filter(work_province="内蒙古自治区")
                for data in data_list:
                    models.NeiMengGu.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "吉林省":
                data_list = models.Data.objects.all().filter(work_province="吉林省")
                for data in data_list:
                    models.JiLin.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "四川省":
                data_list = models.Data.objects.all().filter(work_province="四川省")
                for data in data_list:
                    models.SiChuan.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "天津市":
                data_list = models.Data.objects.all().filter(work_province="天津市")
                for data in data_list:
                    models.TianJin.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "宁夏回族自治区":
                data_list = models.Data.objects.all().filter(work_province="宁夏回族自治区")
                for data in data_list:
                    models.NingXia.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "安徽省":
                data_list = models.Data.objects.all().filter(work_province="安徽省")
                for data in data_list:
                    models.AnHui.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "山东省":
                data_list = models.Data.objects.all().filter(work_province="山东省")
                for data in data_list:
                    models.ShanDong.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "山西省":
                data_list = models.Data.objects.all().filter(work_province="山西省")
                for data in data_list:
                    models.ShanXi_1.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "广东省":
                data_list = models.Data.objects.all().filter(work_province="广东省")
                for data in data_list:
                    models.GuangDong.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "广西壮族自治区":
                data_list = models.Data.objects.all().filter(work_province="广西壮族自治区")
                for data in data_list:
                    models.GuangXi.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "新疆维吾尔自治区":
                data_list = models.Data.objects.all().filter(work_province="新疆维吾尔自治区")
                for data in data_list:
                    models.XinJiang.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "江苏省":
                data_list = models.Data.objects.all().filter(work_province="江苏省")
                for data in data_list:
                    models.JiangSu.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "江西省":
                data_list = models.Data.objects.all().filter(work_province="江西省")
                for data in data_list:
                    models.JiangXi.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "河北省":
                data_list = models.Data.objects.all().filter(work_province="河北省")
                for data in data_list:
                    models.HeBei.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "河南省":
                data_list = models.Data.objects.all().filter(work_province="河南省")
                for data in data_list:
                    models.HeNan.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "浙江省":
                data_list = models.Data.objects.all().filter(work_province="浙江省")
                for data in data_list:
                    models.ZheJiang.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "海南省":
                data_list = models.Data.objects.all().filter(work_province="海南省")
                for data in data_list:
                    models.HaiNan.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "湖北省":
                data_list = models.Data.objects.all().filter(work_province="湖北省")
                for data in data_list:
                    models.HuBei.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "湖南省":
                data_list = models.Data.objects.all().filter(work_province="湖南省")
                for data in data_list:
                    models.HuNan.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "甘肃省":
                data_list = models.Data.objects.all().filter(work_province="甘肃省")
                for data in data_list:
                    models.GanSu.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "福建省":
                data_list = models.Data.objects.all().filter(work_province="福建省")
                for data in data_list:
                    models.FuJian.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "西藏自治区":
                data_list = models.Data.objects.all().filter(work_province="西藏自治区")
                for data in data_list:
                    models.XiZang.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "贵州省":
                data_list = models.Data.objects.all().filter(work_province="贵州省")
                for data in data_list:
                    models.GuiZhou.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "重庆市":
                data_list = models.Data.objects.all().filter(work_province="重庆市")
                for data in data_list:
                    models.ChongQing.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "陕西省":
                data_list = models.Data.objects.all().filter(work_province="陕西省")
                for data in data_list:
                    models.ShanXi_2.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "青海省":
                data_list = models.Data.objects.all().filter(work_province="青海省")
                for data in data_list:
                    models.QingHai.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

            elif province.work_province == "黑龙江省":
                data_list = models.Data.objects.all().filter(work_province="黑龙江省")
                for data in data_list:
                    models.HeiLongJiang.objects.create(
                        id=data.id,
                        ticker=data.ticker,
                        employer=data.employer,
                        title=data.title,
                        salary_range=data.salary_range,
                        a_sala_range_start=data.a_sala_range_start,
                        a_sala_range_end=data.a_sala_range_end,
                        work_experience=data.work_experience,
                        work_location=data.work_location,
                        edu_require=data.edu_require,
                        publish_date=data.publish_date,
                        source=data.source,
                        pos_require=data.pos_require,
                        lang_require=data.lang_require,
                        age_require=data.age_require,
                        employ_type=data.employ_type,
                        year=data.year,
                        day=data.day,
                        count=data.count,
                        industry=data.industry,
                        work_province=data.work_province
                    )

        return JsonResponse({
            "data": "OK"
        })

    def tool_load_employer(self, request):
        _id = 1
        all_data = models.Data.objects.all()
        data_list = all_data.distinct("employer")
        for data in data_list:
            print(data.employer)
            employer_result = all_data.filter(employer=data.employer)
            employer_count = employer_result.count()
            area = employer_result[:1]
            models.Employer.objects.create(
                id=_id,
                name=data.employer,
                area=area[0].work_province,
                employer_count=employer_count
            )
            _id += 1

        return JsonResponse({
            "data": "OK"
        })
