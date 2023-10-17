import json
import random
import time

from browsermobproxy import Server
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from utils import create_chrome_driver, create_chrome_driver_proxy, add_cookies

# 开启代理
BMPserver = Server(r'.\venv\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
BMPserver.start()
BMPproxy = BMPserver.create_proxy()

# 创建 Chrome 浏览器实例
browser = create_chrome_driver_proxy(bMPproxy = BMPproxy)
BMPproxy.new_har("uu",options={'captureContent': True,'captureContent': True})


# 访问网站
browser.get('https://www.youpin898.com/market/csgo?')

# 设置隐式等待
browser.implicitly_wait(10)

add_cookies(browser, 'uu.json')
# 等待一些时间确保 cookie 生效
time.sleep(5)
# 刷新页面
browser.refresh()
time.sleep(2)
# 关闭登录界面
close_btn = browser.find_element(By.CSS_SELECTOR, 'button.ant-modal-close')
close_btn.click()

minPrice_input = browser.find_element(By.CSS_SELECTOR, 'input[placeholder="¥最低价"]')
maxPrice_input = browser.find_element(By.CSS_SELECTOR, 'input[placeholder="¥最高价"]')

# minPrice_input.send_keys('10')
# time.sleep(1)
# maxPrice_input.send_keys('2000')

# 等待页面加载完成
time.sleep(5)  # 等待五秒

har_data = BMPproxy.har


# 循环翻页
total_pages = 100  # 你的翻页总数
result = []

first_iteration = True
save_every = 1  # 每隔多少次循环保存一次数据
counter = 0  # 计数器

for page in range(total_pages):
    if first_iteration:
        # # 执行刷新操作
        # browser.refresh()
        first_iteration = False
    else:
        # 获取翻页按钮
        next_button = browser.find_element(By.CSS_SELECTOR, 'li.ant-pagination-next')

        # 判断是否有遮挡层，如果有，关闭它
        try:
            modal_dialog = browser.find_element(By.CLASS_NAME, 'ant-modal-wrap')
            if modal_dialog.is_displayed():
                # 关闭遮挡层
                close_button = modal_dialog.find_element(By.CLASS_NAME, 'ant-modal-close')
                ActionChains(browser).move_to_element(close_button).click().perform()
        except:
            pass

        time.sleep(random.uniform(5,15))  # 等待一秒
        next_button.click()

    # 等待页面加载完成
    time.sleep(8)

    json_data = BMPproxy.har
    har_data = json_data

    processed_data = []
    for item in har_data['log']['entries']:
        if "response" in item and "content" in item["response"] and "text" in item["response"]["content"]:
            response_text = item["response"]["content"]["text"]
            try:
                response_json = json.loads(response_text)
                if "Code" in response_json and "Data" in response_json and isinstance(response_json["Data"], list):
                    processed_data.extend(response_json["Data"])
            except json.JSONDecodeError:
                print("JSON in response text.")

    result.extend(processed_data[-20:])
    print("有数据：",len(result))
    counter += 1
    if counter == save_every:
        # 将处理后的数据写入 JSON 文件
        output_file_path = "processed_data.json"
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(result, output_file, ensure_ascii=False, indent=4)
        counter = 0  # 重置计数器


print("Processed data has been written to", output_file_path)


# 进入无限循环，直到手动停止循环
while True:
    pass

# 关闭浏览器
browser.quit()
