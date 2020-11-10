import akshare as ak
import matplotlib.pyplot as plt
# 导入柱状图-Bar
from pyecharts.charts import Bar
from pyecharts import options as opts
# print(ak.__version__)

# hist_df = ak.stock_us_daily(symbol="AMZN")  # Get U.S. stock Amazon's price info
# print(hist_df)


# 设置行名
# V1 版本开始支持链式调用
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker

# c = (
#     Pie()
#     .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
#     .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
#     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
#     .render("pie_base.html")
# )

# stock_sse_summary_df = ak.stock_sse_summary();
# x_set = set([]);
# y_item_list = set([]);
# # print(type(stock_sse_summary_df));
#
# for row in stock_sse_summary_df.iterrows():
#     print(row[1])
#     x_set.add(row[1]['type']);
#     item = row[1]['item'].strip().replace("（份）","");
#     y_item_list.add(item);
# y_item_option = [];
# for stock in y_item_list:
#     res2 = [i[1]['number'] for i in stock_sse_summary_df.iterrows() if i[1]['item'].strip().replace("（份）","") == stock]
#     option = {stock: res2};
#     y_item_option.append(option);

stock_szse_summary_df = ak.stock_szse_summary()
# print(stock_szse_summary_df)
category = []
number = []
for row in stock_szse_summary_df.iterrows():
    category.append(row[1]['证券类别'])
    number.append((row[1]['数量(只)']))

print(category)
print(number)
c = (
    Pie()
    .add(
        "",
        [list(z) for z in zip(category, number)],
        center=["35%", "50%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="深交所"),
        legend_opts=opts.LegendOpts(pos_left="15%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"))
)
