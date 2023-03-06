from django.db import models


class Data(models.Model):
    ticker = models.IntegerField()
    employer = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    salary_range = models.CharField(max_length=256)
    a_sala_range_start = models.IntegerField()
    a_sala_range_end = models.IntegerField()
    work_experience = models.CharField(max_length=256)
    work_location = models.CharField(max_length=256)
    edu_require = models.CharField(max_length=256)
    publish_date = models.CharField(max_length=256)
    source = models.CharField(max_length=256)
    pos_require = models.TextField()
    lang_require = models.CharField(max_length=256)
    age_require = models.CharField(max_length=256)
    employ_type = models.CharField(max_length=256)
    year = models.IntegerField()
    day = models.IntegerField()
    count = models.IntegerField()
    industry = models.CharField(max_length=256)
    work_province = models.CharField(max_length=256)

    class Meta:
        db_table = "data"


class ProvinceCityMap(models.Model):
    province = models.CharField(max_length=256)
    city = models.CharField(max_length=256)

    class Meta:
        db_table = "province_city_map"
