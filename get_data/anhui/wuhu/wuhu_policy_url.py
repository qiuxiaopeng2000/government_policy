import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))
import time
from selenium.webdriver.common.by import By
from libs.mysql_util import insert_or_update, select_data
from libs.spyder_util import get_html, parse_page, browserdriver, edgedriver
import random

category_list = ['金融保险', '财政税务', '发展改革', '文化旅游', '农林水利', '市场监管', '科技工信', '住房城建', '医疗卫生', '其它']


sql_select = "select url from gov_url where belong_to = '安徽' and name = '芜湖市'"
gov_url = select_data(sql_select)
url = gov_url[0][0]
print(url)
wd = browserdriver()
wd.get(url)
# 爬取规范性文件
zc_btn = wd.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/a')
zc_btn.click()
gfxwj_btn = wd.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/ul/li[2]/a')
href = gfxwj_btn.get_attribute('href')
print(href)
wd.get(href)

all_policy = []
next_btn = wd.find_element(By.XPATH, '//*[@id="page_public_info_type_xzfgk_tab_0_0"]/a[text()="下一页"]')

num = 0

select_sql = "select create_time from policy_url where belong_to='芜湖市' order by create_time desc limit 1"
last_create_time = select_data(select_sql)
# print(last_create_time)

while next_btn.get_attribute('class') != 'disabled' and num < 3:
    # print(num)
    page_html = wd.page_source
    page_html.encode('utf-8')
    page = parse_page(page_html)
    # 只爬取最新发布的政策
    policy_times = page.xpath('//*[@id="tab_0_0"]/table/tbody/tr/td[2]/p/span[2]/text()')
    index = 0
    flag = False
    if last_create_time is not None:
        last_create_time = last_create_time[0][0]
        for i in range(0, len(policy_times)):
            times = policy_times[i][6:]
            if str(times) <= last_create_time:
                print(times)
                index = i
                flag = True
                break
    if flag:
        policy = page.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/table/tbody/tr')[2:index + 1]
        all_policy.append(policy)
        break

    policy = page.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/table/tbody/tr')[2:]
    print(len(policy))
    all_policy.append(policy)
    next_btn.click()
    time.sleep(2)
    next_btn = wd.find_element(By.XPATH, '//*[@id="page_public_info_type_xzfgk_tab_0_0"]/a[text()="下一页"]')
    num += 1
print(len(all_policy))
wd.close()
print("开始爬取芜湖省颁布的政策链接")
for item in all_policy:
    for provence in item:
        title = provence.xpath('.//a[1]/text()')[0]
        title = ''.join(title.split())
        # print(title)
        href = provence.xpath('.//a[1]/@href')[0]
        belong_to = "芜湖市"
        create_time = provence.xpath('.//span[2]/text()')
        create_time = ''.join(create_time)
        create_time = create_time.replace('|', '')
        category = random.choice(category_list)
        # print(create_time)
        sql = "insert into policy_url(policy_url, policy_title, belong_to, create_time, category) values ('%s', '%s', '%s', '%s', '%s')" % (href, title, belong_to, create_time, category)
        insert_or_update(sql)
print("爬取成功!")
