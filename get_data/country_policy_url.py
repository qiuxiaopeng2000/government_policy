import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
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


url = "http://www.gov.cn/zhengce/xxgk/index.htm"
wd = browserdriver()
wd.get(url)
all_policy = []
next_btn = wd.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[8]')
num = 0
select_sql = "select create_time from policy_url where city='国家' order by create_time desc limit 1"
last_create_time = select_data(select_sql)
while next_btn.get_attribute('class')[-1] != 'whj_hoverDisable' and num < 3:
    print(num)
    page_html = wd.page_source
    page = parse_page(page_html)
    # 只爬取最新发布的政策
    policy_times = page.xpath('//*[@id="xxgkzn_list"]/div[1]/table/tbody/tr/td[5]/text()')
    index = 0
    flag = False
    if last_create_time:
        for i in range(0, len(policy_times)):
            if policy_times[i] <= last_create_time:
                index = i
                flag = True
                break
    if flag:
        policy = page.xpath('/html/body/div[3]/div[2]/div/div[2]/div[1]/div[2]/div[1]/table/tbody/tr')[2:index+1]
        all_policy.append(policy)
        break

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
        city = "国家"
        create_time = provence.xpath('./td[5]/text()')[0]
        category = random.choice(category_list)
        policy_urls = PolicyUrl.objects.create(policy_url=href, policy_title=title, city=city, category=category,
                                               create_time=create_time)
        # sql = "insert into policy_url(policy_url, policy_title, city, create_time, category) values ('%s', '%s', '%s', '%s', '%s')" % (href, title, city, create_time, category)
        # insert_or_update(sql)
print("爬取成功!")
