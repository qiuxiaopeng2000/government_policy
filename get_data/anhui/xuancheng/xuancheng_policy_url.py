import urllib.request
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
from lxml import etree
import random
from libs.mysql_util import insert_or_update

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35",
    "Cookie": "__yjs_duid=1_9b28318f27d0aba28bf56468b5d00f451667978877933; security_session_verify=8a1ce54d776857ec596f88e1a78f9e82; __8qcehdE7ZaRq2q6M__=933f44e982508d1d2c6beab56ed8af14"
}
category_list = ['金融保险', '财政税务', '发展改革', '文化旅游', '农林水利', '市场监管', '科技工信', '住房城建', '医疗卫生', '其它']

print("开始爬虫！")
for index in range(1, 12):
    print("爬取第%s页" % index)
    page1 = requests.get(url='http://www.xuancheng.gov.cn/XxgkPolicy/showList/226/page_' + str(index) + '.html?column=104175&level=1',
                                   headers=header)  # 反爬虫
    page1.encoding = 'utf-8'
    page1 = page1.text
    soup = etree.HTML(page1)
    soup_a = soup.xpath('//*[@id="xxgk_main"]/div/div[2]/ul/li')
    # print(soup_a)
    # soup_a = soup_a[397:428]

    i = 0
    df = pd.DataFrame(columns=['policy_url', 'policy_title', 'city', 'category', 'create_time'])
    for link in soup_a:
        # children_div = link.find_all('div')
        children_a = link.xpath('.//a[1]/@href')[0]
        href = 'http://www.xuancheng.gov.cn' + str(children_a)
        df.loc[i, 'gov_url'] = href
        gov_name = link.xpath('.//a[1]/text()')[0]
        df.loc[i, 'gov_name'] = gov_name
        # children_span = children_div[1].find_all('span')
        city = '宣城市'
        times = link.xpath('./div[2]/div[2]/span[2]/font/text()')[0]
        timeArray = time.strptime(times, "%Y-%m-%d")
        times = time.strftime("%Y-%m-%d", timeArray)
        category = random.choice(category_list)
        sql = "insert into policy_url(policy_url, policy_title, city, category, create_time) values ('%s', '%s', '%s', '%s', '%s')" % (href, gov_name, city, category, times)
        # sql = "insert into data(title, url, create_time, city, category, head, body) values {}" .format(title, url, create_time, city, category, head, body)
        # data = (title, url, create_time, city, category, head, body)
        insert_or_update(sql)  # 插入数据
        time.sleep(2)  # 睡眠
print("爬虫成功！")
