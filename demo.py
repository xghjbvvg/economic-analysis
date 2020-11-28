# from selenium import webdriver
# import time
#
# # 获取一个浏览器对象
# br = webdriver.Chrome()
#
# # 打开一个页面
# br.get('http://data.eastmoney.com/dataapi/invest/other?href=/api/Zgfxzs/json/AnalysisIndexNew.aspx&paramsstr=index%3D1%26size%3D100%26code%3D11000200926')
#
# # 获取页面的源代码（运行后在内存中渲染的页面元素）
# print(br.page_source)
# import os
# import time
# from pathlib import Path
#
# path = str((Path(__file__).parent).absolute()) + "/static/img_" + str(time.time()).replace(".","") + '.png';
# fd = open(path, mode="w", encoding="utf-8")
# fd.close()

# import socket
#
# def get_host_ip():
#     """
#     查询本机ip地址
#     :return: ip
#     """
#     global s;
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 80))
#         ip = s.getsockname()[0]
#     finally:
#         s.close()
#
#     return ip
#
# if __name__ == '__main__':
#     print(get_host_ip())


import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

caps = {
    'browserName': 'chrome',
    'loggingPrefs': {
        'browser': 'ALL',
        'driver': 'ALL',
        'performance': 'ALL',
    },
    'goog:chromeOptions': {
        'perfLoggingPrefs': {
            'enableNetwork': True,
        },
        'w3c': False,
    },
}
driver = webdriver.Chrome(desired_capabilities=caps)

driver.get('http://data.eastmoney.com/invest/invest/11000176275.html')
# 必须等待一定的时间，不然会报错提示获取不到日志信息，因为絮叨等所有请求结束才能获取日志信息
time.sleep(3)

request_log = driver.get_log('performance')
print(request_log)

for i in range(len(request_log)):
    message = json.loads(request_log[i]['message'])
    message = message['message']['params']
    # .get() 方式获取是了避免字段不存在时报错
    request = message.get('request')
    if (request is None):
        continue

    url = request.get('url')
    if (url == "http://data.eastmoney.com/dataapi/invest/other?href=/api/Zgfxzs/json/AnalysisIndexls.aspx&paramsstr=index%3D1%26size%3D100%26code%3D11000176275"):
        # 得到requestId
        print(message['requestId'])
        # 通过requestId获取接口内容
        content = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': message['requestId']})
        print(content)
        break

