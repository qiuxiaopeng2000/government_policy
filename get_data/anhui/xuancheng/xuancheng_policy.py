import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))
import requests
import pandas as pd
import time
from libs.mysql_util import insert_or_update, select_data
from lxml import etree
import django
import os
# from api.views import newDataTest


# print(" ++++++-------")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "government.settings")
django.setup()
from api.models import Data
select_sql = "select create_time from data where city='宣城市' order by create_time desc limit 1"
last_create_time = select_data(select_sql)
last_create_time = last_create_time[0][0]

# sql_select = "select * from policy_url where city='宣城市'"
sql_select = "select * from policy_url where city='宣城市' and create_time > '%s'" % last_create_time
gov_file = select_data(sql_select)
print(len(gov_file))
gov_file = pd.DataFrame(gov_file)
gov_file.columns = ['id', 'policy_url', 'policy_title', 'city', 'category', 'create_time']
# print(gov_file.head())

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35",
    "Cookie": "__yjs_duid=1_9b28318f27d0aba28bf56468b5d00f451667978877933; security_session_verify=8a1ce54d776857ec596f88e1a78f9e82; __8qcehdE7ZaRq2q6M__=933f44e982508d1d2c6beab56ed8af14"
}
print("开始爬取每个政策文件的具体内容")

datas = []
for i in gov_file.index:
    lists = []
    print("爬取第%s个政策" % i)
    url = gov_file.loc[i, 'policy_url']
    title = gov_file.loc[i, 'policy_title']
    create_time = gov_file.loc[i, 'create_time']
    # create_time = time.strptime(create_time, "%Y年%m月%d日")
    # create_time = time.strftime('%Y-%m-%d', create_time)
    # create_time = time.strftime()
    city = gov_file.loc[i, 'city']
    category = gov_file.loc[i, 'category']
    page1 = requests.get(url, headers=header)
    page1.encoding = 'utf-8'
    source = page1.text
    soup = etree.HTML(source)
    head = soup.xpath('/html/body/div[1]/div[3]/div[1]//text()')
    head = '\n'.join(head)
    body = soup.xpath('/html/body/div[1]/div[3]/div[3]//text()')
    body = '\n'.join(body)
    # lists.append(title)
    # lists.append(url)
    # lists.append(create_time)
    # lists.append(city)
    # lists.append(category)
    # lists.append(head)
    # lists.append(body)
    # datas.append(lists)
    # newDataTest(title, url, create_time, city, category, head,body)
    data = Data.objects.create(title=title, url=url, create_time=create_time, city=city, category=category, head=head,
                              body=body)
    # sql = "insert into data(title, url, create_time, city, category, head, body) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (title, url, create_time, city, category, head, body)
    # insert_or_update(sql)
    # time.sleep(2)
print("爬取成功！")
