import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
import time
from selenium.webdriver.common.by import By
from libs.mysql_util import insert_or_update, select_data
from libs.spyder_util import parse_page, browserdriver


sql_select = "select url from gov_url where name = '安徽'"
gov_url = select_data(sql_select)
url = gov_url[0][0]
print(url)
wd = browserdriver()
wd.get(url)
btn = wd.find_element(By.ID, 'organ_catalog_tree_12_a')
btn.click()
new_btn = wd.find_element(By.ID, 'organ_catalog_tree_15_a')
new_btn.click()

all_policy = []
# next_btn_html = page.xpath('/html/body/div[3]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[8]')[0]
next_btn = wd.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/div/div[2]/div/div[3]/a[5]')
num = 0
while next_btn.get_attribute('class') != 'disabled' and num < 3:
    # print(num)
    page_html = wd.page_source
    page_html.encode('utf-8')
    page = parse_page(page_html)
    policy = page.xpath('/html/body/div[1]/div[3]/div/div[2]/div/div[2]/div/div[2]/div')
    print(len(policy))
    all_policy.append(policy)
    next_btn.click()
    time.sleep(2)
    next_btn = wd.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/div/div[2]/div/div[3]/a[5]')
    num += 1
print(len(all_policy))
wd.close()
print("开始爬取安徽省颁布的政策链接")
for item in all_policy:
    for provence in item:
        title = provence.xpath('.//li[3]/a/text()')[0]
        href = provence.xpath('.//li[3]/a/@href')[0]
        belong_to = "安徽"
        create_time = provence.xpath('.//li[2]/text()')[0]
        sql = "insert into policy_url(policy_url, policy_title, belong_to, create_time) values ('%s', '%s', '%s', '%s')" % (href, title, belong_to, create_time)
        insert_or_update(sql)
print("爬取成功!")
