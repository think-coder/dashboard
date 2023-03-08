from django.urls import path

from . import views

urlpatterns = [
    # 检索雇主是否存在
    path('get_employer/<str:employer>/', views.Logic().get_employer, name='get_employer'),
    # 获取雇主总数量
    path('get_total_employer/', views.Logic().get_total_employer, name='get_total_employer'),
    # 获取雇主[区间]
    path('get_employer_by_limit/<int:page>/<int:num>', views.Logic().get_employer_by_limit, name='get_employer_by_limit'),
    # 获取某雇主下，全部招聘信息的数量
    path('get_total_by_employer/<str:employer>', views.Logic().get_total_by_employer, name='get_total_by_employer'),
    # 获取某雇主下，区间招聘信息内容
    path('get_employer_data_by_limit/<str:employer>/<int:page>/<int:num>', views.Logic().get_employer_data_by_limit, name='get_employer_data_by_limit'),
    # 获取所有省份
    path('get_all_province', views.Logic().get_all_province, name='get_all_province'),
    # 获取省份下所有城市
    path('get_city_by_province/<str:province>', views.Logic().get_city_by_province, name='get_city_by_province'),
    # 获取全国HTML图
    path('get_map_by_country/<str:country>', views.Logic().get_map_by_country, name='get_map_by_country'),
    # 获取省份HTML图
    path('get_map_by_province/<str:province>', views.Logic().get_map_by_province, name='get_map_by_province'),
    # 导入数据
    path('load_data', views.Logic().load_data, name='load_data'),
]
