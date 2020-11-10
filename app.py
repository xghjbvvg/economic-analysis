import json

from flask import Flask
from jinja2 import Markup
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from main.config import create_app
import akshare as ak

app = create_app("default")

@app.route("/")
def index():
    return "hello,world"



#
# @app.route("/")
# def index():
#     # Get U.S. stock Amazon's price info
#     stock_sse_summary_df = ak.stock_sse_summary()
#     x_set = set([])
#     y_item_list = set([])
#     # print(type(stock_sse_summary_df));
#
#     for row in stock_sse_summary_df.iterrows():
#         x_set.add(row[1]['type'])
#         item = row[1]['item'].strip().replace("（份）", "")
#         y_item_list.add(item)
#     y_item_option = []
#     for stock in y_item_list:
#         res2 = [i[1]['number'] for i in stock_sse_summary_df.iterrows() if
#                 i[1]['item'].strip().replace("（份）", "") == stock]
#         option = {stock: res2}
#         y_item_option.append(option)
#
#     c = (Bar().add_xaxis(
#         x_set
#     ).set_global_opts(
#         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
#         title_opts=opts.TitleOpts(title="上交所", subtitle="市场详情"),
#         yaxis_opts=opts.AxisOpts(
#             axislabel_opts=opts.LabelOpts(
#                 formatter="{value}")),
#         toolbox_opts=opts.ToolboxOpts(),
#         legend_opts=opts.LegendOpts(is_show=False),
#     ))
#     for row in y_item_option:
#         for key in row:
#             print(key)
#             c.add_yaxis(key, row[key], gap="20%")
#     return Markup(c.render_embed())
#
#
# # 上交所总貌
#
#
@app.route("/shang_stock_exchange")
def shang_stock_exchange():
    # Get U.S. stock Amazon's price info
    stock_sse_summary_df = ak.stock_sse_summary()
    x_set = set([])
    y_item_list = set([])
    # print(type(stock_sse_summary_df));

    for row in stock_sse_summary_df.iterrows():
        x_set.add(row[1]['type'])
        item = row[1]['item'].strip().replace("（份）", "")
        y_item_list.add(item)
    y_item_option = []
    for stock in y_item_list:
        res2 = [i[1]['number'] for i in stock_sse_summary_df.iterrows() if
                i[1]['item'].strip().replace("（份）", "") == stock]
        option = {stock: res2}
        y_item_option.append(option)

    c = (Bar().add_xaxis(
        x_set
    ).set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title="上交所", subtitle="市场详情"),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(
                formatter="{value}")),
        toolbox_opts=opts.ToolboxOpts(),
        legend_opts=opts.LegendOpts(is_show=False),
    ))
    for row in y_item_option:
        for key in row:
            print(key)
            c.add_yaxis(key, row[key], gap="20%")
    return Markup(c.render_embed())


# 深交所
@app.route("/shen_stock_exchange")
def shen_stock_exchange():
    stock_szse_summary_df = ak.stock_szse_summary()
    # print(stock_szse_summary_df)
    category = []
    number = []
    for row in stock_szse_summary_df.iterrows():
        category.append(row[1]['证券类别'])
        number.append((row[1]['数量(只)']))

    c = (
        Pie(init_opts=opts.InitOpts(width="1600px", height="1000px"))
            .add(
            "深交所",
            [list(z) for z in zip(category, number)],
            center=["35%", "50%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="深交所"),
            legend_opts=opts.LegendOpts(pos_left="15%"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
            .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ))

    )

    return Markup(c.render_embed())


if __name__ == '__main__':
    # app = create_app("default")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
