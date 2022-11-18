import requests
from selenium import webdriver
from lxml import etree
import time
import csv


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26",
    "Cookie": "wdcid=7e5f8a4af3a1e4cc; __auc=6dd3455d18422f6a066894998a8; allmobilize=mobile; wdses=0881f840949d8c9c; __asc=cf9242cc184469c56f6dea1c9f4; wdlast=1667633915"
}


def tabluate(tables: list, file_name: str) -> None:
    file_name += ".csv"
    with open(file_name, 'w+', newline='') as csv_out:
        csv_writer = csv.writer(csv_out)
        csv_writer.writerows(tables)


def browserdriver():
    options = webdriver.ChromeOptions()
    out_path = r'D:\QMDownload\data_store'  # 是你想指定的下载路径
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features")    # 反爬虫
    options.add_argument("--disable-blink-features=AutomationControlled")
    # s = Service("C:\\Program Files\\Google\\Chrome\\Application\\chromedriver_win32\\chromedriver.exe")
    wd = webdriver.Chrome(
        executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver_win32\chromedriver.exe',
        options=options)
    return wd


def edgedriver():
    wd = webdriver.Edge(r"C:\Users\Lenovo\.conda\envs\py39\msedgedriver.exe")
    return wd


def get_html(url, wd):
    # wd = browserdriver()
    wd.get(url)
    time.sleep(2)
    return wd.page_source


def parse_page(source):
    page = etree.HTML(source)
    return page


def request(url):
    fail = 1
    while fail < 31:
        try:
            r = requests.get(url, headers=header, timeout=3, verify=False)
            break
        except:
            fail += 1
            time.sleep(1)
    return r.text


