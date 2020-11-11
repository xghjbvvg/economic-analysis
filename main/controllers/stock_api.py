import json

from flask import Blueprint, Flask, abort, jsonify, request
from markupsafe import Markup

from main.config import db
from main.config.ResponseBuilder import ReponseBuilder
from main.config.core import res
from main.dto.userDto import UserDto
import akshare as ak
from jinja2 import Markup
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from main.models.StockAhNameDict import StockAhNameDict

stock_app = Blueprint('stock', __name__, url_prefix='/api/stock')

session = db.session


@stock_app.route('/', methods={'get'})
def offices():
    # abort(403)
    return 'Hello World! my office我的'


@stock_app.route('/user/<int:user_id>', methods={'get'})
def get(user_id):
    print(user_id)
    user = UserDto(id=4, name="hcx", password="123456")
    print(type(user))
    session.add(user)
    session.commit()
    return "success";


@stock_app.route('/stock_zh_ah_name_dict', methods={'get'})
def stock_zh_ah_name_dict():
    print(6)
    stock_zh_ah_name_dict = ak.stock_zh_ah_name();
    stock_list = [];
    for key in stock_zh_ah_name_dict:
        dict_item = StockAhNameDict();
        dict_item.code = key;
        dict_item.name = stock_zh_ah_name_dict[key];
        stock_list.append(dict_item);
    print(stock_list);
    session.add_all(stock_list)
    session.commit()
    return "success"





@stock_app.route("/shang_stock_exchange")
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

    response = ReponseBuilder(True,c.dump_options_with_quotes());
    return json.dumps(response.__dict__);


# 深交所
@stock_app.route("/shen_stock_exchange")
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

