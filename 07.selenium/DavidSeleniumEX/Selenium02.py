from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
 
# available since 2.4.0
from selenium.webdriver.support.ui import WebDriverWait
 
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC


# open the browser
print("===\nopen the browser\n===\n\n\n")
driver = webdriver.Chrome('assets/chromedriver.exe')
# makes sure slower connections work as well        
print ("Waiting 10 sec")
driver.implicitly_wait(10)

# 開啟 google
driver.get("http://www.google.com")
 
# 顯示標題
print(driver.title)
 
# 找到搜尋框
inputElement = driver.find_element_by_name("q")
 
# 搜尋框輸入字
inputElement.send_keys("DavidLanz")
#inputElement.send_keys("DavidLanz site:jumpin.cc")
 
# 送出查詢
inputElement.submit()
 
try:
    # 直到標題有 DavidLanz
    WebDriverWait(driver, 10).until(EC.title_contains("DavidLanz"))
 
    # 顯示標題，可看到 DavidLanz
    print(driver.title)
except TimeoutException:
    print('time out')
finally:
    #driver.quit()
    pass
    
