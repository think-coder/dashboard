from django.urls import path

from . import views

urlpatterns = [
    # 教学评估表
    path('table/teach_assess', views.Edp().teach_assess, name='teach_assess'),
]
