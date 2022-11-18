import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
from libs.mysql_util import insert_or_update
from libs.spyder_util import get_html, parse_page, browserdriver

url = "http://www.gov.cn/zhengce/xxgk/index.htm"
wd = browserdriver()
page_html = get_html(url, wd)
page = parse_page(page_html)
all_provence = page.xpath('/html/body/div[3]/div[2]/div/div[2]/div[5]/div[1]/div/table/tbody//td')
print("开始爬取各省份官网地址")
for provence in all_provence:
    name = provence.xpath('./a/text()')[0]
    name = ''.join(name.split())
    href = provence.xpath('./a/@href')[0]
    belong_to = "国家"
    sql = "insert into gov_url(url, name, belong_to) values ('%s', '%s', '%s')" % (href, name, belong_to)
    insert_or_update(sql)
print("爬取成功!")
wd.close()


