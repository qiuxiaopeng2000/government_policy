import urllib.request
from bs4 import BeautifulSoup
import time
import pandas as pd
from libs.mysql_util import insert_or_update

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35",
    "Cookie": "__yjs_duid=1_9b28318f27d0aba28bf56468b5d00f451667978877933; security_session_verify=8a1ce54d776857ec596f88e1a78f9e82; __8qcehdE7ZaRq2q6M__=933f44e982508d1d2c6beab56ed8af14"
}

print("开始爬虫！")
for index in range(1, 6):
    print("爬取第%s页" % index)
    page1 = urllib.request.Request('http://www.policytop.com/newslist.aspx?fenl=501&twofenl=&page=' + str(index),
                                   headers=header)  # 反爬虫
    page = urllib.request.urlopen(page1)  # 打开网页
    source = page.read()  # 获取网页源代码

    soup = BeautifulSoup(source, 'lxml')
    soup_a = soup.find_all(class_="sup-list-item m-b-md")
    # print(soup_a)
    # soup_a = soup_a[397:428]

    i = 0
    df = pd.DataFrame(columns=['policy_url', 'policy_title', 'belong_to', 'category', 'create_time'])
    for link in soup_a:
        children_div = link.find_all('div')
        children_p = link.find('p')
        href = 'http://www.policytop.com/newsview.aspx?num=' + str(children_div[0].attrs['onclick'])[7:-2]
        df.loc[i, 'gov_url'] = href
        gov_name = children_div[0].find('span').get_text()
        df.loc[i, 'gov_name'] = gov_name
        children_span = children_div[1].find_all('span')
        city = children_span[0].get_text()[5:]
        times = children_span[5].get_text()[5:]
        timeArray = time.strptime(times, "%Y/%m/%d")
        times = time.strftime("%Y-%m-%d", timeArray)
        category = children_div[2].get_text()[6:]
        sql = "insert into policy_url(policy_url, policy_title, belong_to, category, create_time) values ('%s', '%s', '%s', '%s', '%s')" % (href, gov_name, city, category, times)
        # sql = "insert into data(title, url, create_time, city, category, head, body) values {}" .format(title, url, create_time, city, category, head, body)
        # data = (title, url, create_time, city, category, head, body)
        insert_or_update(sql)  # 插入数据
        time.sleep(2)  # 睡眠
print("爬虫成功！")
