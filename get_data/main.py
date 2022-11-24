import os
import time


# Python try块不会捕获os.system异常
def spider_country():
    os.system('python F:/研究生/课设/government_policy/country_policy_url.py')
    os.system('python F:/研究生/课设/government_policy/country_policy.py')


def spider_anhui():
    start_time = time.time()
    ret = os.system('python F:/研究生/课设/government_policy/get_data/anhui/provence_policy_url.py && python F:/研究生/课设/government_policy/get_data/anhui/provence_policy.py' + " 2>out2.txt")
    # ret1 = os.system('' + " 2>out1.txt")
    if ret != 0:
        os.system('python F:/研究生/课设/government_policy/get_data/all_provence_url.py')
        os.system('python F:/研究生/课设/government_policy/get_data/anhui/provence_policy_url.py')
        os.system('python F:/研究生/课设/government_policy/anhui/provence_policy.py')
    end_time = time.time()
    print('total time: ', end_time - start_time)


def spider_wuhu():
    ret = os.system('python F:/研究生/课设/government_policy/get_data/anhui/wuhu/wuhu_policy_url.py' + " 2>out1.txt")
    ret1 = os.system('python F:/研究生/课设/government_policy/get_data/anhui/wuhu/wuhu_policy.py' + " 2>out.txt")
    if ret != 0 and ret1 != 0:
        os.system('python F:/研究生/课设/government_policy/get_data/all_provence_url.py')
        os.system('python F:/研究生/课设/government_policy/get_data/anhui/all_city_url.py')
        os.system('python F:/研究生/课设/government_policy/get_data/anhui/wuhu/wuhu_policy_url.py')
        os.system('python F:/研究生/课设/government_policy/get_data/anhui/wuhu/wuhu_policy.py')


