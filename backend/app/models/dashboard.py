# -*- coding:utf-8 -*-
import pyecharts.options as opts
from pyecharts.charts import Map

class Dashboard(object):
    def __init__(self):
        self.html_file = "./test-xray.html"

    def get_dashboard(self):
        province_data = [
            ['河南省', 45.23], ['北京市', 37.56],
            ['河北省', 21], ['辽宁省', 12],
            ['江西省', 6], ['上海市', 20],
            ['安徽省', 10], ['江苏省', 16],
            ['湖南省', 9], ['浙江省', 13],
            ['海南省', 2], ['广东省', 22],
            ['湖北省', 8], ['黑龙江省', 11],
            ['澳门特别行政区', 1], ['陕西省', 11],
            ['四川省', 7], ['内蒙古', 3],
            ['重庆市', 3], ['云南省', 6],
            ['贵州省', 2], ['吉林省', 3],
            ['山西省', 12], ['山东省', 11],
            ['福建省', 4], ['青海省', 1],
            ['天津市', 1], ['其他', 1],
        ]
        d_map = (
            Map()
            .add(
                series_name="每上市公司平均招聘数量",
                maptype="china",
                data_pair=province_data,

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
                    title="2017年全国各省级区域每上市公司平均招聘数量",
                    pos_left='30%',
                    pos_top='10'
                ),
                visualmap_opts=opts.VisualMapOpts(
                    min_=0,
                    max_=50,
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
            .render(path=self.html_file)
        )

        html_file = open(self.html_file, "r").read()
        return html_file
