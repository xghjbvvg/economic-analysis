import json

from flask import Blueprint, Flask, abort, jsonify, request
from main.config import db, stock_zh_a_new_col
from main.config.ResponseBuilder import ReponseBuilder
from main.config.core import redis, redis_menu
from main.dto.userDto import UserDto
import akshare as ak
from jinja2 import Markup
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from main.models.StockAhNameDict import StockAhNameDict
from models.StockZhANew import StockZhANew

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


# 获取AH上市字典集合
@stock_app.route('/stock_zh_ah_name_dict', methods={'get'})
def stock_zh_ah_name_dict():
    stock_info_a_code_name_df = ak.stock_info_a_code_name();
    stock_list = [];
    # 当前股票字典
    for row in stock_info_a_code_name_df.iterrows():
        dict_item = StockAhNameDict();
        dict_item.code = row[1]['code'];
        dict_item.name = row[1]['name'];
        stock_list.append(dict_item);

    # 本地mysql股票字典
    # mysql_stock_info = session.query(StockAhNameDict).all();
    num_rows_deleted = db.session.query(StockAhNameDict).delete()
    print(num_rows_deleted);

    session.add_all(stock_list);
    session.commit();
    response = ReponseBuilder(True, "success");
    return json.dumps(response.__dict__);


# 获取次新股
@stock_app.route("/stock_zh_a_new")
def stock_zh_a_new():
    stock_zh_a_new_df = ak.stock_zh_a_new();
    stock_list = [];
    print(type(stock_zh_a_new_df));
    stock_zh_a_new_col.delete_many({});
    for row in stock_zh_a_new_df.iterrows():
        dict_item = StockZhANew();
        # 新浪代码
        dict_item.symbol = row[1]['symbol'];
        # 股票代码
        dict_item.code = row[1]['code'];
        #股票简称
        dict_item.name = row[1]['name'];
        # 开盘价
        dict_item.open = row[1]['open'];
        # 最高价
        dict_item.high = row[1]['high'];
        # 最低价
        dict_item.low = row[1]['low'];
        # 成交量
        dict_item.volume = row[1]['volume'];
        # 成交额
        dict_item.amount = row[1]['amount'];
        # 市值
        dict_item.mktcap = row[1]['mktcap'];
        # 换手率
        dict_item.turnoverratio = row[1]['turnoverratio'];
        stock_list.append(dict_item.__dict__);


    # print(json.dumps(stock_list));

    x = stock_zh_a_new_col.insert_many(stock_list);
    # # # 输出插入的所有文档对应的 _id 值
    print(x.inserted_ids);
    response = ReponseBuilder(True, "success");
    return json.dumps(response.__dict__);


# 上交所
@stock_app.route("/shang_stock_exchange")
def shang_stock_exchange():
    res = redis.get(redis_menu + "shang_stock_exchange");
    print(res);
    if res is not None:
        # redis 中存在redsi键值
        return res;
    else:
        # 不存在
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
            title_opts=opts.TitleOpts(title="上交所总貌", subtitle="市场详情"),
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

        response = ReponseBuilder(True, c.dump_options_with_quotes());
        resJson = json.dumps(response.__dict__);
        redis.setex(redis_menu + "shang_stock_exchange", 3600*24, resJson)
        return resJson;


# 深交所
@stock_app.route("/sheng_stock_exchange")
def shen_stock_exchange():
    res = redis.get(redis_menu + "sheng_stock_exchange");
    print(res);
    if res is not None:
        return res;
    else:

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
                "深交所总貌",
                [list(z) for z in zip(category, number)],
                center=["35%", "50%"],
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="深交所总貌"),
                legend_opts=opts.LegendOpts(pos_left="15%"),
            )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
                .set_series_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                ))

        )
        response = ReponseBuilder(True, c.dump_options_with_quotes());
        resJson = json.dumps(response.__dict__)
        redis.setex(redis_menu + "sheng_stock_exchange", 3600*24, resJson);
        return resJson;
