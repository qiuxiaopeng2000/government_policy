import os
import sys

import requests

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))
import pandas as pd
import time
from libs.spyder_util import parse_page
from libs.mysql_util import insert_or_update, select_data
from libs.header import set_header
from concurrent.futures import ThreadPoolExecutor


def get_wuhu(i):
    # wd = browserdriver()
    header = set_header()
    url = gov_file.loc[i, 'policy_url']
    title = gov_file.loc[i, 'policy_title']
    create_time = gov_file.loc[i, 'create_time']
    city = gov_file.loc[i, 'city']
    category = gov_file.loc[i, 'category']
    source = requests.get(url=url, headers=header, verify=False).text
    source.encoding = 'utf-8'
    # source = get_html(url, wd)
    soup = parse_page(source)
    head = soup.xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/div[1]/table[2]/tbody//text()')
    # print('成功')
    head = '\n'.join(head)
    body = soup.xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[1]//text()')
    body = '\n'.join(body)
    # print(body[0:8])
    sql = "insert into data(title, url, create_time, city, category, head, body) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (title, url, create_time, city, category, head, body)
    insert_or_update(sql)
    # time.sleep(2)
    # wd.close()


sql_select = "select * from policy_url where city = '芜湖市'"
gov_file = select_data(sql_select)
gov_file = pd.DataFrame(gov_file)
gov_file.columns = ['id', 'policy_url', 'policy_title', 'city', 'category', 'create_time']
print(len(gov_file))

# header = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35",
#     "Cookie": "__yjs_duid=1_9b28318f27d0aba28bf56468b5d00f451667978877933; security_session_verify=8a1ce54d776857ec596f88e1a78f9e82; __8qcehdE7ZaRq2q6M__=933f44e982508d1d2c6beab56ed8af14"
# }

start = time.time()
print("开始爬取每个政策文件的具体内容")
pool = ThreadPoolExecutor(max_workers=8)
for index in gov_file.index:
    # print(index)
    pool.submit(get_wuhu, index)
    # get_wuhu(index)
print("爬取成功！")
end = time.time()
print(end - start)
pool.shutdown(wait=True)
