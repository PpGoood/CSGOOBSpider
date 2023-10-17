import json

from fake_useragent import UserAgent
from selenium import  webdriver
import time
import random
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options




# def create_chrome_driver(*,headless = False):
#     options = webdriver.ChromeOptions()
#     if headless:
#         options.add_argument('--headless')
#     options.add_experimental_option('excludeSwitches',['enable-automation'])
#     options.add_experimental_option('useAutomationExtension',False)
#     browser = webdriver.Chrome(options = options)
#     browser.execute_cdp_cmd(
#         'Page.addScriptToEvaluateOnNewDocument',
#         {'source':'Object.defineProperty(navigator,"webdriver",{get:()=> undefined})'}
#     )
#     return browser
def create_chrome_driver_proxy(*, headless=False,bMPproxy):
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    #禁止大量无效日志
    options.options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # 禁用扩展插件，因为我也不是太懂，总之没了这句，浏览器会报警提示如下图。魔法，勿动。
    options.add_argument('--ignore-certificate-errors')
    # BMPproxy.proxy返回的是localhost:8081端口
    options.add_argument('--proxy-server={}'.format(bMPproxy.proxy))

    browser = webdriver.Chrome(options=options)
    browser.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=> undefined})'}
    )
    return browser
def create_chrome_driver(*, headless=False):
    download_dir = r'G:\Desktop\python项目\uuDemo\dataExcel'  #

    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    options = Options()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_dir}
    options.add_experimental_option("prefs", prefs)
    if headless:
        options.add_argument('--headless')

    #user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    # 创建UserAgent对象
    # ua = UserAgent()
    # # 使用指定的User-Agent字符串生成伪装的User-Agent
    # fake_user_agent = ua.random
    # options.add_argument(f"user-agent={fake_user_agent}")
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    browser = webdriver.Chrome(options=options)
    browser.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=> undefined})'}
    )
    return browser

def add_cookies(browser, cookie_file):
    with open(cookie_file, 'r') as file:
        cookie_list = json.load(file)
        for cookie_dict in cookie_list:
            # 检查Cookie的名称是否匹配
            if 'name' in cookie_dict and cookie_dict['name'] in ['token', 'Hm_lpvt_339d14d4beac3e390c97656a27dc4b25','_uab_collina','NTKF_T2D_CLIENTID','Hm_lvt_339d14d4beac3e390c97656a27dc4b25','nTalk_CACHE_DATA']:
                # 确保cookie的domain与正在访问的域名匹配
                if 'domain' in cookie_dict and cookie_dict['domain'] in browser.current_url:
                    browser.add_cookie(cookie_dict)
                    print(f"Cookie {cookie_dict['name']} 已成功注入")






