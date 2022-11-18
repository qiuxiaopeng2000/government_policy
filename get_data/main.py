import os


# 待处理：重复爬取
# Python try块不会捕获os.system异常
def spider_country():
    ret = os.system('python F:/Python/government/get_data/country_policy.py' + " 2>out.txt")
    if ret != 0:
        os.system('python F:/Python/government/get_data/country_policy_url.py')
        os.system('python F:/Python/government/get_data/country_policy.py')


def spider_anhui():
    ret = os.system('python F:/Python/government/get_data/anhui/provence_policy.py' + " 2>out.txt")
    if ret != 0:
        os.system('python F:/Python/government/get_data/all_provence_url.py')
        os.system('python F:/Python/government/get_data/anhui/provence_policy_url.py')
        os.system('python F:/Python/government/get_data/anhui/provence_policy.py')


def spider_wuhu():
    ret = os.system('python F:/Python/government/get_data/anhui/wuhu/wuhu_policy.py' + " 2>out.txt")
    if ret != 0:
        os.system('python F:/Python/government/get_data/all_provence_url.py')
        os.system('python F:/Python/government/get_data/anhui/all_city_url.py')
        os.system('python F:/Python/government/get_data/anhui/wuhu/wuhu_policy_url.py')
        os.system('python F:/Python/government/get_data/anhui/wuhu/wuhu_policy.py')


