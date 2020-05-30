# 蝦皮查詢商品
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
 
# available since 2.4.0
from selenium.webdriver.support.ui import WebDriverWait
 
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC

prefs = {"profile.default_content_setting_values.notifications" : 2}

# open the browser with options
print("===\nopen the browser\n===\n\n\n")
chrome_options = Options()
# chrome_options.add_argument('--dns-prefetch-disable')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--lang=en-US')
# chrome_options.add_argument('--headless')

# 停用瀏覽器上的顯示提醒 Notification 功能
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")
#chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US', 'default_content_setting_values': {'notifications': 2}} )
chrome_options.add_experimental_option("prefs",prefs)

# browser = webdriver.Chrome(executable_path='D:/Programming/Python/Selenium/assets/chromedriver.exe', chrome_options=chrome_options)
# browser = webdriver.Chrome(executable_path='D:/Programming/Python/Selenium/assets/geckodriver.exe', chrome_options=chrome_options)
driver = webdriver.Chrome('assets/chromedriver.exe', chrome_options=chrome_options)
# makes sure slower connections work as well        
print ("Waiting 10 sec")
driver.implicitly_wait(10)

# 開啟 蝦皮
driver.get("https://shopee.tw/")

# 顯示標題
print(driver.title)

#重新整理網頁
driver.refresh()

time.sleep(2)
# 找到搜尋框
# inputElement = driver.find_elements_by_class_name("shopee-searchbar-input__input")
# 以上會回傳list，是錯誤的寫法!

# 寫法一: 不適合
#inputElement = driver.find_element_by_xpath('.//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/form/input')

# 寫法二: 找尋id或class的名稱
inputElement = driver.find_element_by_xpath(".//*[@class='shopee-searchbar-input__input']")

# 其他可用尋找的方法
# find_elements_by_id
# find_elements_by_class_name

# 搜尋框輸入字
inputElement.send_keys("鐵三角 ATH-AR5BT")
#inputElement.send_keys("DavidLanz site:jumpin.cc")

# 送出查詢 (錯誤的表單，因為採用的是DOM)
#inputElement.submit()

# 按下按鈕
inputElement = driver.find_element_by_xpath('.//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/button')
#driver.find_element_by_css_selector("[class^='btn btn-solid-primary']").click()
#inputElement = driver.find_element_by_xpath("//button[.='送出']") # 若按鈕有文字的話
inputElement.click()

try:
    # 直到標題有 ATH-AR5BT
    WebDriverWait(driver, 10).until(EC.title_contains("ATH-AR5BT"))
 
    # 顯示標題，可看到 ATH-AR5BT
    print(driver.title)
    #存下畫面圖檔
    time.sleep(2)
    driver.save_screenshot('Selenium05_screenshots.png')
    
    productElement = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/button')
    #h4[class='entry-title'] > a
    #a[class='post-thumbnail']
    #//div[@class="listRight"]/ul/li/h2/a/text()
    #//div[@class="listRight"]/ul/li/h2/a/@href
    #//div[@class="listRight"]/ul/li/div/time/@datetime
    #//html/body/dt/a/img/@src
    #//*[@class="one"]/ul/li
    #//span[@class='class']

    list_item = driver.find_elements_by_xpath('//*[@class="shopee-item-card__text-name"]')
    print(len(list_item))
    for x in list_item:
        print(x.text)

except TimeoutException:
    print('time out')
finally:
    driver.quit()
    pass
    
