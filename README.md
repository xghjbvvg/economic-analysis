# economic-analysis

# 系统某些功能需要安装chromedriver.exe，集成MySQL，Mongodb以及Redis，都在app.py中已配置

# api接口：
## 总貌 /api/stock/
* /stock_zh_ah_name_dict：获取AH上市字典集合，系统是会自动更新
* /stock_zh_a_new  获取次新股 ，进入系统时会自动更新
* /shang_stock_exchange 上交所总貌 （图标显示）
* /sheng_stock_exchange 深交所总貌 （图标显示）

## 分析师详情 /api/account
 * /detail 获取每月新增投资人折线图
 * /analyst_rank 分析师排名榜,前50
 */analyst_info/<int:code> 获取投资人股票详情，使用selenium进行数据爬取，并且进行截图显示

