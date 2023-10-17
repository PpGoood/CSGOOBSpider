import time

from utils import create_chrome_driver, add_cookies

browser = create_chrome_driver()
browser.get('https://www.youpin898.com/')
# 添加 cookie 到浏览器
add_cookies(browser, 'uu.json')
# 等待一些时间确保 cookie 生效
time.sleep(8)
browser.refresh()
# 访问网站
browser.get('https://www.youpin898.com/goodInfo?id=243')
time.sleep(1)  # 等待五秒
# 刷新页面
browser.refresh()
# # 等待一些时间确保页面加载完全
# time.sleep(5)
#
# # 访问另一个页面
# browser.get('https://www.youpin898.com/goodInfo?id=101433')

# 进入无限循环，直到手动停止循环
while True:
    pass
