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

class ProvinceMaptype(models.Model):
    province = models.CharField(max_length=256)
    maptype = models.CharField(max_length=256)

    class Meta:
        db_table = "province_maptype"


class Employer(models.Model):
    name = models.CharField(max_length=256)
    area = models.CharField(max_length=256)
    employer_count = models.IntegerField()

    class Meta:
        db_table = "employer"


class ShangHai(Data):
    class Meta:
        db_table = "shanghai"


class YunNan(Data):
    class Meta:
        db_table = "yunnan"


class NeiMengGu(Data):
    class Meta:
        db_table = "neimenggu"


class BeiJing(Data):
    class Meta:
        db_table = "beijing"


class JiLin(Data):
    class Meta:
        db_table = "jilin"


class SiChuan(Data):
    class Meta:
        db_table = "sichuan"


class TianJin(Data):
    class Meta:
        db_table = "tianjin"


class NingXia(Data):
    class Meta:
        db_table = "ningxia"


class AnHui(Data):
    class Meta:
        db_table = "anhui"


class ShanDong(Data):
    class Meta:
        db_table = "shandong"


class GuangXi(Data):
    class Meta:
        db_table = "guangxi"


class GuangDong(Data):
    class Meta:
        db_table = "guangdong"


class ShanXi_1(Data):
    class Meta:
        db_table = "shanxi_1"


class XinJiang(Data):
    class Meta:
        db_table = "xinjiang"


class JiangSu(Data):
    class Meta:
        db_table = "jiangsu"


class JiangXi(Data):
    class Meta:
        db_table = "jiangxi"


class HeBei(Data):
    class Meta:
        db_table = "hebei"


class HeNan(Data):
    class Meta:
        db_table = "henan"


class ZheJiang(Data):
    class Meta:
        db_table = "zhejiang"


class HuBei(Data):
    class Meta:
        db_table = "hubei"


class HaiNan(Data):
    class Meta:
        db_table = "hainan"


class HuNan(Data):
    class Meta:
        db_table = "hunan"


class GanSu(Data):
    class Meta:
        db_table = "gansu"


class FuJian(Data):
    class Meta:
        db_table = "fujian"


class XiZang(Data):
    class Meta:
        db_table = "xizang"


class GuiZhou(Data):
    class Meta:
        db_table = "guizhou"


class LiaoNing(Data):
    class Meta:
        db_table = "liaoning"


class ChongQing(Data):
    class Meta:
        db_table = "chongqing"


class ShanXi_2(Data):
    class Meta:
        db_table = "shanxi_2"


class QingHai(Data):
    class Meta:
        db_table = "qinghai"


class HeiLongJiang(Data):
    class Meta:
        db_table = "heilongjiang"


class Year2017(Data):
    class Meta:
        db_table = "data_2017"


class Year2018(Data):
    class Meta:
        db_table = "data_2018"


class Year2019(Data):
    class Meta:
        db_table = "data_2019"


class Year2020(Data):
    class Meta:
        db_table = "data_2020"


class Year2021(Data):
    class Meta:
        db_table = "data_2021"


class Year2022(Data):
    class Meta:
        db_table = "data_2022"
