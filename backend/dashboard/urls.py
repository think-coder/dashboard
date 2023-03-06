from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_employer/<str:employer>/', views.get_employer, name='get_employer'),
    path('get_total_employer/', views.get_total_employer, name='get_total_employer'),
    path('get_employer_by_limit/<int:page>/<int:num>', views.get_employer_by_limit, name='get_employer_by_limit'),
    path('get_total_by_employer/<str:employer>', views.get_total_by_employer, name='get_total_by_employer'),
    path('get_employer_data_by_limit/<str:employer>/<int:page>/<int:num>', views.get_employer_data_by_limit, name='get_employer_data_by_limit'),
    path('get_all_province', views.get_all_province, name='get_all_province'),
    path('get_city_by_province/<str:province>', views.get_city_by_province, name='get_city_by_province'),
    path('get_map_by_country/<str:country>', views.get_map_by_country, name='get_map_by_country'),
    path('get_map_by_province/<str:province>', views.get_map_by_province, name='get_map_by_province'),
    path('load_data', views.load_data, name='load_data'),
]
