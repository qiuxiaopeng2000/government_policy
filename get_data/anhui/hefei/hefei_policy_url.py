import time
from selenium.webdriver.common.by import By

from libs.mysql_util import insert_or_update, select_data
from libs.spyder_util import get_html, parse_page, browserdriver, edgedriver

sql_select = "select * from gov_url where belong_to = '安徽' and name = '合肥市'"
gov_url = select_data(sql_select)
url = gov_url[0][0]
print(url)
wd = browserdriver()
wd.get(url)
time.sleep(5)
# 爬取规范性文件
zc_btn = wd.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div[1]/div/dl[1]/a')
zc_btn.click()
gfxwj_btn = wd.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div[1]/div/div[1]/ul/li[2]/a')
gfxwj_btn.click()

all_policy = []
next_btn = wd.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[3]')
num = 0
while next_btn.get_attribute('class') != 'disabled' and num < 3:
    print(num)
    page_html = wd.page_source
    page_html.encode('utf-8')
    page = parse_page(page_html)
    policy = page.xpath('/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[2]')[2:]
    print(len(policy))
    all_policy.append(policy)
    next_btn.click()
    time.sleep(2)
    next_btn = wd.find_element(By.CSS_SELECTOR, 'div#page_public_info a:nth-child(8)')
    num += 1
print(len(all_policy))
wd.close()
print("开始爬取安徽省颁布的政策链接")
for item in all_policy:
    for provence in item:
        title = provence.xpath('.//a[1]/text()')[0]
        href = "https://www.hefei.gov.cn/" + provence.xpath('.//a[1]/@href')[0]
        belong_to = "合肥市"
        create_time = provence.xpath('.//li[2]/text()')[0]
        sql = "insert into policy_url(policy_url, policy_title, belong_to, create_time) values ('%s', '%s', '%s', '%s')" % (href, title, belong_to, create_time)
        insert_or_update(sql)
print("爬取成功!")
