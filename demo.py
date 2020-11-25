import json

import akshare as ak

from config import stock_analyst_rank_col
from config.core import redis, redis_menu
from models.AnalystRank import AnalystRank

flag = redis.get(redis_menu + "tock_analyst_rank");
analystRankList = [];
if flag  is not None:

    analystRankList = stock_analyst_rank_col.find();
else:
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
        analystRank.stockName = row[1]['NewIndex'];
        # # 3个月收益率
        analystRank.earnings_3 = row[1]['Earnings_3'];
        # # 6个月收益率
        analystRank.earnings_6 = row[1]['Earnings_6'];
        # # 12个月收益率
        analystRank.earnings_12 = row[1]['Earnings_12'];
        # # 2020最新个股评级
        analystRank.newGgpj = row[1]['NewGgpj'];
        # # 2020最新个股评级
        analystRank.stockcount = row[1]['stockcount'];

        analystRank.fxsCode = row[1]['FxsCode'];


        analystRankList.append(analystRank.__dict__);

    stock_analyst_rank_col.insert_many(analystRankList);
    redis.setex(redis_menu + "tock_analyst_rank", 3600 * 12, "1")
    print(analystRankList)


for x in analystRankList:
  print(x)


