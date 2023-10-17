import json
import random
import time

from browsermobproxy import Server
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from utils import create_chrome_driver, create_chrome_driver_proxy

# 开启代理



# 创建 Chrome 浏览器实例
browser = create_chrome_driver()

# 访问网站
browser.get('https://www.youpin898.com/market/csgo?')

# 设置隐式等待
browser.implicitly_wait(10)

# 用户输入账号
username_input = browser.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入手机账号"]')
username_input.send_keys('13971853583')

# 获取验证码按钮点击
get_code_button = browser.find_element(By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.ant-btn-lg.ant-input-search-button')
time.sleep(1)  # 等待一秒
get_code_button.click()

# 等待用户手动输入验证码
verification_code = input("Please enter the verification code: ")

# 用户输入验证码
password_input = browser.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入短信验证码"]')
password_input.send_keys(verification_code)
time.sleep(1)  # 等待一秒

# 找到登录/注册按钮并点击
login_button = browser.find_element(By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.ant-btn-lg.ant-btn-block')
login_button.click()

time.sleep(8)  # 等待五秒

# 获取 cookie 并保存到文件
with open('../uu.json', 'w') as file:
    json.dump(browser.get_cookies(), file)
    print("写入cookie的json文件")



time.sleep(3)  # 等待五秒

# 关闭浏览器
browser.quit()
