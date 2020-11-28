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

import socket

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    global s;
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

if __name__ == '__main__':
    print(get_host_ip())
