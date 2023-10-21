import selenium

print(selenium.__version__)

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--disable-popup-blocking")

driver = webdriver.Chrome(options=options)
driver.get('http://www.baidu.com')
print(driver.current_url)
print(driver.page_source)