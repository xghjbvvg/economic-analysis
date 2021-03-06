import json
import os
from pathlib import Path
import socket


from bs4 import BeautifulSoup
from selenium import webdriver
import akshare as ak
import pyecharts.options as opts
from pyecharts.charts import Line

from app import stock_analyst_rank_col, rootpath, app_port
from config.core import redis, redis_menu
from models.AnalystRank import AnalystRank
from bson import json_util
import time

def stock_em_account_detail():
    account_json = redis.get(redis_menu + "stock_em_account");
    if account_json is not None:
        print(account_json);
        # redis 中存在redsi键值
        account = json.loads(account_json);
        date = account['date'];
        new_investors_number = account["stock_account_num"];
    else:

        stock_em_account_df = ak.stock_em_account();
        print(stock_em_account_df)

        date = []
        new_investors_number = []

        for row in stock_em_account_df.iterrows():
            date.append(row[1]['数据日期'])
            new_investors_number.append(row[1]['新增投资者-数量'])
        account_dict = {};
        date.reverse();
        new_investors_number.reverse();
        account_dict['date'] = date;
        account_dict["stock_account_num"] = new_investors_number;
        redis.setex(redis_menu + "stock_em_account", 3600*24*30, json.dumps(account_dict))


    c = (
        Line(init_opts=opts.InitOpts(width="1680px", height="800px"))
        .add_xaxis(date)
        .add_yaxis(
            series_name="新增投资者-数量",
            y_axis=new_investors_number,

            is_smooth=True,
            is_symbol_show=False,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="股票账户统计月度"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            # datazoom_opts=[
            #     opts.DataZoomOpts(yaxis_index=0),
            #     opts.DataZoomOpts(type_="inside", yaxis_index=0),
            # ],
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(

                type_="value",
                name="万",
                name_location="start",
                min_=0,
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
            ),
        )

    )
    return c



def stock_em_analyst_rank():
    flag = redis.get(redis_menu + "tock_analyst_rank");
    analystRankList = [];
    if flag is not None:

        analystRank = stock_analyst_rank_col.find({}).sort("lastYearSyl",-1);
        # analystRank.sort(key=lambda x: x.lastYearSyl)
        return json_util.dumps(analystRank);
    else:
        stock_analyst_rank_col.delete_many({});
        stock_em_analyst_rank_df = ak.stock_em_analyst_rank()
        for row in stock_em_analyst_rank_df.iterrows():
            analystRank = AnalystRank();
            # 2020年收益率
            analystRank.lastYearSyl = row[1]['LastYearSyl'];
            # # 股票名称
            analystRank.stockName = row[1]['StockName'];
            # # 姓名
            analystRank.fxsName = row[1]['FxsName'];
            # # 单位
            analystRank.ssjg = row[1]['Ssjg'];
            # # 年度指数
            analystRank.newIndex = row[1]['NewIndex'];
            # # 3个月收益率
            analystRank.earnings_3 = row[1]['Earnings_3'];
            # # 6个月收益率
            analystRank.earnings_6 = row[1]['Earnings_6'];
            # # 12个月收益率
            analystRank.earnings_12 = row[1]['Earnings_12'];
            # # 2020最新个股评级
            analystRank.newGgpj = row[1]['NewGgpj'];
            # # 成分股个数
            analystRank.stockcount = row[1]['stockcount'];

            analystRank.fxsCode = row[1]['FxsCode'];

            analystRankList.append(analystRank.__dict__);

        stock_analyst_rank_col.insert_many(analystRankList);
        analystRankList.sort(key=lambda x: x['lastYearSyl'], reverse=True)
        redis.setex(redis_menu + "tock_analyst_rank", 3600 * 12, "1");
        return json_util.dumps(analystRankList);


def stock_em_analyst_info(code):
    # 获取一个浏览器对象
    br = webdriver.Chrome()

    # 打开一个页面
    br.get(
        'http://data.eastmoney.com/dataapi/invest/other?href=/api/Zgfxzs/json/AnalysisIndexNew.aspx&paramsstr=index%3D1%26size%3D100%26code%3D'+str(code))

    # 获取页面的源代码（运行后在内存中渲染的页面元素）
    soup = BeautifulSoup(br.page_source, 'lxml')
    br.close();
    ss = soup.select('pre')[0]
    res = ss.text;
    return res;


def stock_em_analyst_exponent(code):
    # 获取一个浏览器对象
    br = webdriver.Chrome()
    br.set_window_size(1200, 900)
    # 打开一个页面
    br.get('http://data.eastmoney.com/invest/invest/'+str(code)+'.html');
    # time.sleep(1)
    ele = br.find_element_by_class_name('fContent');
    # ele = br.find_element_by_id("flash")
    filename = "/static/img_" + str(code) + '.png';
    path = rootpath + filename;
    if os.path.exists(path):
        os.remove(path);
    file = open(path, mode="w", encoding="utf-8")
    file.close()
    ele.screenshot(path)  # 元素截图
    br.close();

    return "http://"+get_host_ip()+":"+str(app_port)+filename;

def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()

    return ip