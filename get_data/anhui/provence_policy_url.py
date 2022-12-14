import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
import time
from selenium.webdriver.common.by import By
from libs.mysql_util import insert_or_update, select_data
from libs.spyder_util import parse_page, browserdriver
import random
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "government.settings")
django.setup()
from api.models import PolicyUrl


category_list = ['金融保险', '财政税务', '发展改革', '文化旅游', '农林水利', '市场监管', '科技工信', '住房城建', '医疗卫生', '其它']


select_sql = "select create_time from policy_url where city='安徽' order by create_time desc limit 1"
last_create_time = select_data(select_sql)
# time.sleep(2)
# print('last_create_time: ', last_create_time)

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
    # 只爬取最新发布的政策
    policy_times = page.xpath('//*[@id="xxgk_lmcon"]/div[2]/div/ul/li[3]/span/text()')
    index = 0
    flag = False
    if last_create_time is not None:
        last_create_time = last_create_time[0][0]
        print(last_create_time)
        for i in range(0, len(policy_times)):
            if str(policy_times[i]) <= last_create_time:
                print(str(policy_times[i]))
                index = i
                flag = True
                break
    if flag:
        policy = page.xpath('/html/body/div[1]/div[3]/div/div[2]/div/div[2]/div/div[2]/div')[0:index + 1]
        all_policy.append(policy)
        break

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
        city = "安徽"
        create_time = provence.xpath('.//li[2]/text()')[0]
        category = random.choice(category_list)
        policy_urls = PolicyUrl.objects.create(policy_url=href, policy_title=title, city=city, category=category, create_time=create_time)
        # policy_url.save()
        # sql = "insert into policy_url(policy_url, policy_title, city, create_time, category) values ('%s', '%s', '%s', '%s', '%s')" % (href, title, city, create_time, category)
        # insert_or_update(sql)
print("爬取成功!")


