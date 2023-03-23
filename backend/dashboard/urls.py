from django.urls import path

from . import views

urlpatterns = [
    # 注册
    path('user/registry', views.Logic().registry, name='registry'),
    # 登录
    path('user/login', views.Logic().login, name='login'),
    # 登出
    path('user/logout', views.Logic().logout, name='logout'),
    # 获取验证码图片
    path('resource/image_code/<str:code_uuid>', views.Logic().get_image_code, name='get_image_code'),
    # 检索雇主是否存在
    path('resource/get_employer/<str:employer>', views.Logic().get_employer, name='get_employer'),
    # 获取雇主总数量
    path('resource/get_total_employer', views.Logic().get_total_employer, name='get_total_employer'),
    # 获取雇主[区间]
    path('resource/get_employer_by_limit/<int:page>/<int:num>', views.Logic().get_employer_by_limit, name='get_employer_by_limit'),
    # 获取某雇主下，全部招聘信息的数量
    path('resource/get_total_by_employer/<str:employer>', views.Logic().get_total_by_employer, name='get_total_by_employer'),
    # 获取某雇主下，区间招聘信息内容
    path('resource/get_employer_data_by_limit/<str:employer>/<int:page>/<int:num>', views.Logic().get_employer_data_by_limit, name='get_employer_data_by_limit'),
    # 获取所有省份
    path('resource/get_all_province', views.Logic().get_all_province, name='get_all_province'),
    # 获取省份下所有城市
    path('resource/get_city_by_province/<str:province>', views.Logic().get_city_by_province, name='get_city_by_province'),
    # 获取全国HTML图
    path('resource/get_map_by_country/<str:country>', views.Logic().get_map_by_country, name='get_map_by_country'),
    # 获取省份HTML图
    path('resource/get_map_by_province/<str:province>', views.Logic().get_map_by_province, name='get_map_by_province'),
    # 获取一线/新一线HTML图
    path('resource/get_map_of_top_city', views.Logic().get_map_of_top_city, name='get_map_of_top_city'),
    # 获取需求增加最快的15种岗位HTML图
    path('resource/get_map_of_top_rise', views.Logic().get_map_of_top_rise, name='get_map_of_top_rise'),
    # 获取需求下降最快的15种岗位HTML图
    path('resource/get_map_of_tail_reduce', views.Logic().get_map_of_tail_reduce, name='get_map_of_tail_reduce'),

    # 导入数据
    path('tool/load_data', views.Logic().tool_load_data, name='tool_load_data'),
    # 导入年份数据
    path('tool/load_data_by_year', views.Logic().tool_load_data_by_year, name='tool_load_data_by_year'),
    # 导入省份数据
    path('tool/load_data_by_province', views.Logic().tool_load_data_by_province, name='tool_load_data_by_province'),
    # 导入雇主数据
    path('tool/load_employer', views.Logic().tool_load_employer, name='tool_load_employer'),

    # 任务: 生成国级HTML文件
    path('job/generate_country_map', views.Logic().job_generate_country_map, name='job_generate_country_map'),
    # 任务: 生成省级HTML文件
    path('job/generate_province_map', views.Logic().job_generate_province_map, name='job_generate_province_map'),
    # 任务: 生成一线/新一线HTML文件
    path('job/generate_columnar_map', views.Logic().job_generate_columnar_map, name='job_generate_columnar_map'),
    # 任务: 生成需求增加/下降最快的15种岗位
    path('job/generate_map_of_rise_reduce', views.Logic().job_generate_map_of_rise_reduce, name='job_generate_map_of_rise_reduce'), 
]
