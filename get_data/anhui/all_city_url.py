import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
from libs.mysql_util import insert_or_update, select_data
from libs.spyder_util import get_html, parse_page, browserdriver
from libs.header import set_header

header = set_header()
sql_select = "select url from gov_url where name = '安徽'"
gov_url = select_data(sql_select)
# print(len(gov_url))
url = gov_url[0][0]
wd = browserdriver()
page1 = get_html(url, wd)
page1_html = parse_page(page1)
href = page1_html.xpath('/html/body/div[1]/div[3]/div/div[2]/div/div[1]/div/div[11]/a/@href')[0]
# print(href)

new_url = 'https://www.ah.gov.cn' + href
# print(new_url)
page = get_html(new_url, wd)
# page.encoding = 'utf-8'
page_html = parse_page(page)
all_city = page_html.xpath('//*[@id="container"]/div[3]/div/div[2]/div[2]/div[2]/div/div[4]//a')
# print(len(all_city))

print("开始爬取安徽省官网地址")
for city in all_city:
    name = city.xpath('./text()')[0]
    name = ''.join(name.split())
    href = city.xpath('./@href')[0]
    belong_to = "安徽"
    sql = "insert into gov_url(url, name, belong_to) values ('%s', '%s', '%s')" % (href, name, belong_to)
    insert_or_update(sql)
print("爬取成功!")
wd.close()



