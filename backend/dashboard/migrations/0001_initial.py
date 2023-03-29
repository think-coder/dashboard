# Generated by Django 4.0 on 2023-03-28 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.IntegerField()),
                ('employer', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('salary_range', models.CharField(max_length=256)),
                ('a_sala_range_start', models.IntegerField()),
                ('a_sala_range_end', models.IntegerField()),
                ('work_experience', models.CharField(max_length=256)),
                ('work_location', models.CharField(max_length=256)),
                ('edu_require', models.CharField(max_length=256)),
                ('publish_date', models.CharField(max_length=256)),
                ('source', models.CharField(max_length=256)),
                ('pos_require', models.TextField()),
                ('lang_require', models.CharField(max_length=256)),
                ('age_require', models.CharField(max_length=256)),
                ('employ_type', models.CharField(max_length=256)),
                ('year', models.IntegerField()),
                ('day', models.IntegerField()),
                ('count', models.IntegerField()),
                ('industry', models.CharField(max_length=256)),
                ('work_province', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'data',
            },
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('area', models.CharField(max_length=256)),
                ('employer_count', models.IntegerField()),
            ],
            options={
                'db_table': 'employer',
            },
        ),
        migrations.CreateModel(
            name='ProvinceCityMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'province_city_map',
            },
        ),
        migrations.CreateModel(
            name='ProvinceMaptype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=256)),
                ('maptype', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'province_maptype',
            },
        ),
        migrations.CreateModel(
            name='YearList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'year_list',
            },
        ),
        migrations.CreateModel(
            name='AnHui',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'anhui',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='BeiJing',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'beijing',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='ChongQing',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'chongqing',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='FuJian',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'fujian',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='GanSu',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'gansu',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='GuangDong',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'guangdong',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='GuangXi',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'guangxi',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='GuiZhou',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'guizhou',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='HaiNan',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'hainan',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='HeBei',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'hebei',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='HeiLongJiang',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'heilongjiang',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='HeNan',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'henan',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='HuBei',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'hubei',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='HuNan',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'hunan',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='JiangSu',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'jiangsu',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='JiangXi',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'jiangxi',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='JiLin',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'jilin',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='LiaoNing',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'liaoning',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='NeiMengGu',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'neimenggu',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='NingXia',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'ningxia',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='QingHai',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'qinghai',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='ShanDong',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'shandong',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='ShangHai',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'shanghai',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='ShanXi_1',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'shanxi_1',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='ShanXi_2',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'shanxi_2',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='SiChuan',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'sichuan',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='TianJin',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'tianjin',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='XinJiang',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'xinjiang',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='XiZang',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'xizang',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='Year2017',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'data_2017',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='Year2018',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'data_2018',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='Year2019',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'data_2019',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='Year2020',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'data_2020',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='Year2021',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'data_2021',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='Year2022',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'data_2022',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='YunNan',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'yunnan',
            },
            bases=('dashboard.data',),
        ),
        migrations.CreateModel(
            name='ZheJiang',
            fields=[
                ('data_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.data')),
            ],
            options={
                'db_table': 'zhejiang',
            },
            bases=('dashboard.data',),
        ),
    ]