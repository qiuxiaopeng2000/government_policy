import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
import time
from selenium.webdriver.common.by import By
from libs.mysql_util import insert_or_update
from libs.spyder_util import parse_page, browserdriver

url = "http://www.gov.cn/zhengce/xxgk/index.htm"
wd = browserdriver()
wd.get(url)
all_policy = []
next_btn = wd.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[8]')
num = 0
while next_btn.get_attribute('class')[-1] != 'whj_hoverDisable' and num < 3:
    print(num)
    page_html = wd.page_source
    page = parse_page(page_html)
    policy = page.xpath('/html/body/div[3]/div[2]/div/div[2]/div[1]/div[2]/div[1]/table/tbody/tr')[2:]
    all_policy.append(policy)
    next_btn.click()
    time.sleep(2)
    next_btn = wd.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[8]')
    num += 1
wd.close()
print(len(all_policy))
print("开始爬取国务院颁布的政策链接")
for item in all_policy:
    for provence in item:
        title = provence.xpath('.//a/text()')[0]
        href = provence.xpath('.//a/@href')[0]
        belong_to = "国家"
        create_time = provence.xpath('./td[5]/text()')[0]
        sql = "insert into policy_url(policy_url, policy_title, belong_to, create_time) values ('%s', '%s', '%s', '%s')" % (href, title, belong_to, create_time)
        insert_or_update(sql)
print("爬取成功!")
