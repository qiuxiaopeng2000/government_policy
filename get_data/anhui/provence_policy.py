import requests
import pandas as pd
# import time
# from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
from libs.mysql_util import insert_or_update, select_data
from lxml import etree
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "government.settings")
django.setup()
from api.models import Data


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35",
    "Cookie": "__yjs_duid=1_9b28318f27d0aba28bf56468b5d00f451667978877933; security_session_verify=8a1ce54d776857ec596f88e1a78f9e82; __8qcehdE7ZaRq2q6M__=933f44e982508d1d2c6beab56ed8af14"
}


def get_anhui(i):
    url = gov_file.loc[i, 'policy_url']
    title = gov_file.loc[i, 'policy_title']
    create_time = gov_file.loc[i, 'create_time']
    city = gov_file.loc[i, 'city']
    category = gov_file.loc[i, 'category']
    page1 = requests.get(url, headers=header, verify=False)
    page1.encoding = 'utf-8'
    source = page1.text
    soup = etree.HTML(source)
    head = soup.xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/table/tbody//text()')
    head = '\n'.join(head)
    body = soup.xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]//text()')
    body = '\n'.join(body)
    data = Data.objects.create(title=title, url=url, create_time=create_time, city=city, category=category, head=head, body=body)
    # sql = "insert into data(title, url, create_time, city, category, head, body) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (title, url, create_time, city, category, head, body)
    # insert_or_update(sql)


# sql_select = "select * from policy_url where city = '安徽'"
sql_select = "select * from policy_url where policy_url.city = '安徽' and policy_url.create_time > (select create_time from data where city='安徽' order by create_time desc limit 1)"
gov_file = select_data(sql_select)
gov_file = pd.DataFrame(gov_file)
gov_file.columns = ['id', 'policy_url', 'policy_title', 'city', 'category', 'create_time']
# print(gov_file.head())

pool = ThreadPoolExecutor(10)
print("开始爬取安徽省每个政策文件的具体内容")
for index in gov_file.index:
    # print('爬取第%s个政策文件' % index)
    pool.submit(get_anhui, index)
    # t = Thread(target=get_anhui, args=(index,))
    # t.start()
    # time.sleep(2)
print("爬取成功！")
pool.shutdown(wait=True)


