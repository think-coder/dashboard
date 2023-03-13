import os
import pyecharts.options as opts
from pyecharts.charts import Map, Bar, Timeline
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from dashboard import models


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
        data_list = models.ProvinceCityMap.objects.all().distinct("province")
        per_list = [["", 0]]
        for data in data_list:
            province = data.province
            pos_count = models.Data.objects.filter(year=year).filter(work_province=province).count()
            employer_count = models.Data.objects.filter(year=year).filter(work_province=province).distinct("employer").count()
            if not pos_count or not employer_count:
                return per_list
            per = round(pos_count / employer_count, 1)
            per_list.append([province, per])
        return per_list

    def compute_city_per(self, province, year):
        """计算省级平均招聘量"""
        data_list = models.ProvinceCityMap.objects.filter(province__icontains=province).distinct("city")
        per_list = [["", 0]]
        for data in data_list:
            city = data.city
            pos_count = models.Data.objects.filter(year=year).filter(work_province__icontains=province).filter(work_location=city).count()
            employer_count = models.Data.objects.filter(year=year).filter(work_province__icontains=province).filter(work_location=city).distinct("employer").count()
            if not pos_count or not employer_count:
                return per_list
            per = round(pos_count / employer_count, 1)
            per_list.append([city, per])
        return per_list

    def compute_rise_per(self, title):
        """计算增长率"""
        left_point = models.Data.objects.filter(year='2017').filter(title=title).count()
        right_point = models.Data.objects.filter(year='2021').filter(title=title).count()
        if not left_point or not right_point:
            per = round(right_point ** 1/4 - 1, 1)
        else:
            per = round((right_point / left_point) ** 1/4 - 1, 1)
        return (per, title)


class Logic(object):
    def __init__(self):
        self.file_name = "{file_name}.html"
        self.save_path = "./dashboard/templates/"

    def get_employer(self, request, employer):
        """检索雇主是否存在"""
        data = models.Data.objects.filter(employer__icontains = employer).distinct("employer")
        employer_list = [i.employer for i in data]

        return JsonResponse({
            "data": employer_list
        })

    def get_total_employer(self, request):
        """获取雇主总数"""
        data = models.Data.objects.all().distinct("employer").count()

        return JsonResponse({
            "data": data
        })

    def get_employer_by_limit(self, request, page, num):
        """获取区间雇主列表"""
        # data_total = Data.objects.all().distinct("employer").count()
        # data_employer = Data.objects.all().distinct("employer")[int(page)*(int(num)-1):int(page)*int(num)+int(num)]
        # employer_list = [i.employer for i in data_employer]

        # return JsonResponse({
        #     "total": data_total,
        #     "data": employer_list
        # })

        # 测试：暂时使用
        employer_list = [
            "GQY视讯",
            "GQY视讯股份有限公司",
            "TCL华星光电技术有限公司",
            "TCL华瑞照明科技(惠州)有限公司",
            "TCL华瑞照明科技（惠州）有限公司",
            "TCL商用信息科技(惠州)股份有限公司",
            "TCL奥博(天津)环保发展有限公司",
            "TCL家用电器(中山)有限公司",
            "TCL家用电器（中山）有限公司",
            "TCL家用电器(合肥)有限公司",
            "TCL德龙家用电器(中山)有限公司",
            "TCL德龙家用电器（中山）有限公司",
            "TCL数码科技",
            "TCL显示科技(惠州)",
            "TCL智慧工业(惠州)有限公司",
            "TCL海外电子(惠州)有限公司",
            "TCL王牌电器(惠州)有限公司",
            "TCL王牌电器(成都)有限公司",
            "TCL王牌电器（成都）有限公司",
            "TCL王牌电器（无锡）有限公司",
            "TCL瑞智（惠州）制冷设备有限公司",
            "TCL电子",
            "TCL电子控股有限公司",
            "TCL科技产业园有限公司",
            "TCL科技集团股份有限公司",
            "TCL空调器（中山）有限公司",
            "TCL空调器（武汉）有限公司",
            "TCL通力电子",
            "TCL通力电子(惠州)有限公司",
            "TCL通讯",
            "TCL通讯（宁波）有限公司",
            "TCL通讯科技",
            "TCL金融",
            "TCL金融控股集团",
            "TCL金融控股集团（广州）有限公司",
            "TCL集团",
            "TCL集团工业研究院",
            "TCL集团财务有限公司",
            "TSC集团控股有限公司",
            "一号车市控股有限公司",
            "一品红",
            "一品红药业",
            "一品红药业股份有限公司",
            "一心堂",
            "一心堂药业集团股份有限公司",
            "一拖国际经济贸易有限公司",
            "一拖（洛阳）柴油机有限公司",
            "一拖(洛阳)福莱格车身有限公司",
            "一汽东机工减振器有限公司",
            "一汽光洋转向装置有限公司",
            "一汽奔腾轿车有限公司",
            "一汽富维",
            "一汽富维本特勒汽车零部件(天津)有限公司",
            "一汽富维本特勒汽车零部件（天津）有限公司",
            "一汽海马汽车有限公司",
            "一汽财务有限公司",
            "一汽轿车",
            "一汽轿车股份有限公司",
            "一石巨鑫有限公司",
            "一联易招科技（上海）有限公司",
            "一起住好房(北京)网络科技有限公司",
            "一起住好房（北京）网络科技有限公司",
            "一重集团大连工程建设有限公司",
            "一重集团天津重工有限公司",
            "一重集团常州华冶轧辊有限公司",
            "七一二",
            "七天四季酒店（广州）有限公司",
            "七彩化学股份有限公司",
            "万东医疗",
            "万丰镁瑞丁新材料科技有限公司",
            "万兴科技",
            "万兴科技股份有限公司",
            "万兴科技集团股份有限公司",
            "万华化学",
            "万华化学(北京)有限公司",
            "万华化学(宁波)容威聚氨酯有限公司",
            "万华化学(宁波)有限公司",
            "万华化学(宁波)氯碱有限公司",
            "万华化学(福建)有限公司",
            "万华化学集团股份有限公司",
            "万华集团",
            "万向电动汽车有限公司",
            "万向财务有限公司",
            "万向通达股份公司",
            "万向钱潮",
            "万向钱潮(上海)汽车系统有限公司",
            "万向钱潮（上海）汽车系统有限公司",
            "万向钱潮传动轴有限公司",
            "万向钱潮汽车系统",
            "万向钱潮股份有限公司",
            "万向钱潮股份有限公司等速驱动轴厂",
            "万向钱潮重庆汽车部件有限公司",
            "万孚（吉林）生物技术有限公司",
            "万宁日用品商业（上海）有限公司",
            "万宁连锁商业（北京）有限公司",
            "万宁（重庆）健康产品有限公司",
            "万安科技",
            "万安集团",
            "万安集团有限公司",
            "万家基金"]
        return JsonResponse({
            "total": 10000,
            "data": employer_list
        })

    def get_total_by_employer(self, request, employer):
        """根据雇主名称获取招聘数量"""
        data = models.Data.objects.filter(employer=employer).count()

        return JsonResponse({
            "data": data
        })

    def get_employer_data_by_limit(self, request, employer, page, num):
        """获取雇主的区间数据"""
        # data_total = Data.objects.filter(employer=employer).count()
        # data_employer = Data.objects.filter(employer=employer)[int(page)*(int(num)-1):int(page)*int(num)+int(num)]
        # employer_list = list()
        # for i in data_employer:
        #     employer_list.append({
        #         "股票代码": i.ticker,
        #         "雇主名称": i.employer,
        #         "职位名称": i.title,
        #         "薪资范围": i.salary_range,
        #         "年薪下限": i.a_sala_range_start,
        #         "年薪上限": i.a_sala_range_end,
        #         "工作经验要求": i.work_experience,
        #         "工作地点": i.work_location,
        #         "学历要求": i.edu_require,
        #         "发布日期": i.publish_date,
        #         "语言要求": i.lang_require,
        #         "年龄要求": i.age_require,
        #         "雇主所在行业": i.industry,
        #         "职责描述": i.pos_require,
        #         "任职要求": i.pos_require
        #     })

        data_total = 50
        employ_list = [
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "技术支持/运维工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "经验不限",
                "工作地点": "上海市",
                "学历要求": "学历不限",
                "发布日期": "2021-05-31 15:06:14",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "测试工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "1-3年",
                "工作地点": "上海市",
                "学历要求": "大专及以上",
                "发布日期": "2021-05-12 17:11:36",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "技术支持/运维工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "经验不限",
                "工作地点": "上海市",
                "学历要求": "学历不限",
                "发布日期": "2021-05-31 15:06:14",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "测试工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "1-3年",
                "工作地点": "上海市",
                "学历要求": "大专及以上",
                "发布日期": "2021-05-12 17:11:36",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "技术支持/运维工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "经验不限",
                "工作地点": "上海市",
                "学历要求": "学历不限",
                "发布日期": "2021-05-31 15:06:14",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "测试工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "1-3年",
                "工作地点": "上海市",
                "学历要求": "大专及以上",
                "发布日期": "2021-05-12 17:11:36",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "技术支持/运维工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "经验不限",
                "工作地点": "上海市",
                "学历要求": "学历不限",
                "发布日期": "2021-05-31 15:06:14",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "测试工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "1-3年",
                "工作地点": "上海市",
                "学历要求": "大专及以上",
                "发布日期": "2021-05-12 17:11:36",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "技术支持/运维工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "经验不限",
                "工作地点": "上海市",
                "学历要求": "学历不限",
                "发布日期": "2021-05-31 15:06:14",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "测试工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "1-3年",
                "工作地点": "上海市",
                "学历要求": "大专及以上",
                "发布日期": "2021-05-12 17:11:36",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "技术支持/运维工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "经验不限",
                "工作地点": "上海市",
                "学历要求": "学历不限",
                "发布日期": "2021-05-31 15:06:14",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "测试工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "1-3年",
                "工作地点": "上海市",
                "学历要求": "大专及以上",
                "发布日期": "2021-05-12 17:11:36",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "技术支持/运维工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "经验不限",
                "工作地点": "上海市",
                "学历要求": "学历不限",
                "发布日期": "2021-05-31 15:06:14",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "测试工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "1-3年",
                "工作地点": "上海市",
                "学历要求": "大专及以上",
                "发布日期": "2021-05-12 17:11:36",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "技术支持/运维工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "经验不限",
                "工作地点": "上海市",
                "学历要求": "学历不限",
                "发布日期": "2021-05-31 15:06:14",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "测试工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "1-3年",
                "工作地点": "上海市",
                "学历要求": "大专及以上",
                "发布日期": "2021-05-12 17:11:36",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "技术支持/运维工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "经验不限",
                "工作地点": "上海市",
                "学历要求": "学历不限",
                "发布日期": "2021-05-31 15:06:14",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "测试工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "1-3年",
                "工作地点": "上海市",
                "学历要求": "大专及以上",
                "发布日期": "2021-05-12 17:11:36",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "技术支持/运维工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "经验不限",
                "工作地点": "上海市",
                "学历要求": "学历不限",
                "发布日期": "2021-05-31 15:06:14",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            },
            {
                "股票代码": 300076,
                "雇主名称": "GQY视讯",
                "职位名称": "测试工程师",
                "薪资范围": "6-8k",
                "年薪下限": 6000,
                "年薪上限": 8000,
                "工作经验要求": "1-3年",
                "工作地点": "上海市",
                "学历要求": "大专及以上",
                "发布日期": "2021-05-12 17:11:36",
                "语言要求": "语言不限",
                "年龄要求": "年龄不限",
                "雇主所在行业": "计算机",
                "pos_text": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限",
                "pos_require": "职责描述：1、软硬件产品测试2、产品说明书整理3、样机组装4、操作系统、常用软件安装5、工程项目跟进任职要求：1、计算机相关专业2、熟悉电脑组装，熟悉常见电脑硬件3、有视音频经验优先4、有网络配置经验有限"
            }
        ]

        return JsonResponse({
            "total": data_total,
            "data": employ_list[(int(page) - 1) * int(num): int(page)*int(num)]
        })

    def get_all_province(self, request):
        """获取所有省份名称"""
        res_data = models.ProvinceCityMap.objects.all().distinct("province")
        province_list = [i.province for i in res_data]

        return JsonResponse({
            "data": province_list
        })

    def get_city_by_province(self, request, province):
        """获取省份下属市县名称"""
        res_data = models.ProvinceCityMap.objects.filter(province=province)
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

    def get_map_of_top_city(self, request):
        """获取一线/新一线HTML图"""
        if os.path.exists(self.save_path + self.file_name.format(file_name="新一线")):
            return render(request, self.file_name.format(file_name="新一线"), {})

        self.generate_map_of_top_city()

        return render(request, self.file_name.format(file_name="新一线"), {})

    def get_map_of_top_rise(self, request):
        """获取需求增加最快的15种岗位"""
        if os.path.exists(self.save_path + self.file_name.format(file_name="增长最快")):
            return render(request, self.file_name.format(file_name="增长最快"), {})

        self.generate_map_of_top_rise()

        return render(request, self.file_name.format(file_name="增长最快"), {})

    def get_map_of_tail_reduce(self, request):
        """获取需求下降最快的15种岗位"""
        if os.path.exists(self.save_path + self.file_name.format(file_name="下降最快")):
            return render(request, self.file_name.format(file_name="下降最快"), {})

        self.generate_map_of_tail_reduce()

        return render(request, self.file_name.format(file_name="下降最快"), {})

    def generate_country_map(self, country):
        """生成国级HTML文件"""
        print("### Country: {} ###".format(country))
        year_list = [i.year for i in models.Data.objects.all().distinct("year")]
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
        year_list = [i.year for i in models.Data.objects.all().distinct("year")]
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
        top_city_list = [
            "北京市", "上海市", "广州市", "深圳市",
            "成都市", "重庆市", "杭州市", "西安市", "武汉市",
            "苏州市", "郑州市", "南京市", "天津市", "长沙市",
            "东莞市", "宁波市", "佛山市", "合肥市", "青岛市"
        ]
        per_list = []
        for city in top_city_list:
            print(city)
            pos_count = models.Data.objects.filter(work_location=city).count()
            employer_count = models.Data.objects.filter(work_location=city).distinct("employer").count()
            if not pos_count or not employer_count:
                per_list.append(0)
                continue
            per_list.append(round(pos_count / employer_count, 1))
        print("per_list: {}".format(per_list))

        d_bar = (
            Bar()
            .add_xaxis(top_city_list)
            .add_yaxis("每上市公司平均招聘量", per_list)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="一线/新一线城市每上市公司平均招聘量", subtitle=""),
                xaxis_opts=opts.AxisOpts(name="城市名称"),
                yaxis_opts=opts.AxisOpts(name="每上市公司平均招聘量")
            )
            .render(self.save_path + self.file_name.format(file_name="新一线"))
        )

    def generate_map_of_top_rise(self):
        """生成需求增加最快的15种岗位"""
        title_list = [i.title for i in models.Data.objects.distinct("title")]
        per_list = list()
        map_dict = dict()
        for i in title_list:
            left_point = models.Data.objects.filter(year='2017').filter(title=i).count()
            right_point = models.Data.objects.filter(year='2021').filter(title=i).count()
            if not left_point or not right_point:
                per = round(right_point ** 1/4 - 1, 1)
            else:
                per = round((right_point / left_point) ** 1/4 - 1, 1)

            per_list.append(per)
            map_dict[str(per)] = i

        top_per_list = per_list.sort()[0:15]
        t_list = [map_dict.get(str(per)) for per in top_per_list]
        d_bar = (
            Bar()
            .add_xaxis(t_list)
            .add_yaxis("每上市公司平均招聘量", top_per_list)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="需求增加最快的15种岗位", subtitle=""),
                xaxis_opts=opts.AxisOpts(name="职位"),
                yaxis_opts=opts.AxisOpts(name="增长率")
            )
            .render(self.save_path + self.file_name.format(file_name="增长最快"))
        )
    
    def generate_map_of_tail_reduce(self):
        """生成需求下降最快的15种岗位"""
        title_list = [i.title for i in models.Data.objects.distinct("title")]
        per_list = list()
        map_dict = dict()
        for i in title_list:
            left_point = models.Data.objects.filter(year='2017').filter(title=i).count()
            right_point = models.Data.objects.filter(year='2021').filter(title=i).count()
            if not left_point or not right_point:
                per = round(right_point ** 1/4 - 1, 1)
            else:
                per = round((right_point / left_point) ** 1/4 - 1, 1)

            per_list.append(per)
            map_dict[str(per)] = i

        tail_per_list = per_list.sort()[-15:]
        t_list = [map_dict.get(str(per)) for per in tail_per_list]
        d_bar = (
            Bar()
            .add_xaxis(t_list)
            .add_yaxis("每上市公司平均招聘量", tail_per_list)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="需求下降最快的15种岗位", subtitle=""),
                xaxis_opts=opts.AxisOpts(name="职位"),
                yaxis_opts=opts.AxisOpts(name="增长率")
            )
            .render(self.save_path + self.file_name.format(file_name="增长最快"))
        )

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

    def tool_generate_country_map(self, request):
        """任务: 生成国级HTML文件"""
        print("Begin: tool_generate_country_map")
        self.generate_country_map("中国")
        print("End: tool_generate_country_map")

        return JsonResponse({
            "data": "OK"
        })

    def tool_generate_province_map(self, request):
        """任务: 生成省级HTML文件"""
        print("Begin: tool_generate_province_map")
        res_data = models.ProvinceCityMap.objects.all().distinct("province")
        province_list = [i.province for i in res_data]
        print(len(province_list), province_list)
        
        # 构建线程池，批处理任务
        pool = ThreadPoolExecutor(max_workers=10)
        all_task=[pool.submit(self.generate_province_map, (i)) for i in province_list]
        wait(all_task, return_when=ALL_COMPLETED)
        pool.shutdown()
        print("End: tool_generate_province_map")

        return JsonResponse({
            "data": "OK"
        })

    def tool_generate_columnar_map(self, request):
        """任务: 生成一线/新一线HTML文件"""
        print("Begin: tool_generate_columnar_map")
        self.generate_map_of_top_city()
        print("End: tool_generate_columnar_map")

        return 

    def tool_generate_map_of_rise_reduce(self, request):
        """任务: 生成需求增加/下降最快的15种岗位"""
        _start = time.time()
        print("Begin: tool_generate_map_of_rise_reduce")
        title_list = [i.title for i in models.Data.objects.distinct("title")]
        per_list = list()
        map_dict = dict()

        _num = 1
        executor = ThreadPoolExecutor(max_workers=20)
        for per, title in executor.map(Compute().compute_rise_per, title_list):
            per_list.append(per)
            map_dict[str(per)] = title
            print(_num, title, per)
            _num += 1

        per_list.sort()
        top_per_list = per_list[0:15]
        tail_per_list = per_list[-15:]
        top_list = [map_dict.get(str(per)) for per in top_per_list]
        tail_list = [map_dict.get(str(per)) for per in tail_per_list]
        rise_bar = (
            Bar()
            .add_xaxis(top_list)
            .add_yaxis("每上市公司平均招聘量", top_per_list)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="需求增长最快的15种岗位", subtitle=""),
                xaxis_opts=opts.AxisOpts(name="职位"),
                yaxis_opts=opts.AxisOpts(name="增长率")
            )
            .render(self.save_path + self.file_name.format(file_name="增长最快"))
        )
        reduce_bar = (
            Bar()
            .add_xaxis(tail_list)
            .add_yaxis("每上市公司平均招聘量", tail_per_list)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="需求下降最快的15种岗位", subtitle=""),
                xaxis_opts=opts.AxisOpts(name="职位"),
                yaxis_opts=opts.AxisOpts(name="增长率")
            )
            .render(self.save_path + self.file_name.format(file_name="下降最快"))
        )
        _end = time.time()
        print("End: tool_generate_map_of_rise_reduce")
        print("Total: {}".format(_end - _start))

        return JsonResponse({
            "data": "OK"
        })

    def tool_load_data_by_year(self, request):
        year_list = [2017, 2018, 2019, 2020, 2021, 2022]
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

        return 

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

        return
            
