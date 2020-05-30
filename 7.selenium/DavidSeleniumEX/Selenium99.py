from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
 
# available since 2.4.0
from selenium.webdriver.support.ui import WebDriverWait
 
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC


# open the browser
print("===\nopen the browser\n===\n\n\n")
import os

#Chrome
# chrome_options = Options()
# chrome_options.add_argument('--dns-prefetch-disable')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--lang=en-US')
# chrome_options.add_argument('--headless')
# chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})
# #browser = webdriver.Chrome(executable_path='D:/Programming/Python/Selenium/assets/geckodriver.exe', chrome_options=chrome_options)
# driver = webdriver.Chrome('assets/chromedriver.exe')
# # makes sure slower connections work as well        
# print ("Waiting 10 sec")
# driver.implicitly_wait(10)

# Firefox
# 若 geckodriver 有在 PATH 中， firefox 可不帶路徑參數

'''
On Unix systems you can do the following to append it to your system's search path, if you’re using a bash-compatible shell:

export PATH=$PATH:/path/to/directory/of/executable/downloaded/in/previous/step
On Windows you will need to update the Path system variable to add the full directory path to the executable geckodriver manually or command line(don't forget to restart your system after adding executable geckodriver into system PATH to take effect). The principle is the same as on Unix.
'''

driver = webdriver.Firefox(executable_path='D:/Programming/Python/Selenium/assets/geckodriver.exe')

#IE
# driver = webdriver.Ie('/path/to/Iedriver')

# 可更改 firefox 的 profile
profile = webdriver.FirefoxProfile()
profile.native_events_enabled = True
driver = webdriver.Firefox(profile)

# 目前網址
driver.current_url

# 截圖
driver.save_screenshot('screenshots.png')

# 原始碼 driver.page_source
with open('test.html','wb') as f:
    f.write(driver.page_source.encode('utf-8'))

# 標題
driver.title

# 重新整理
driver.refresh()

# 關閉目前視窗
driver.close()

# 結束全部視窗
driver.quit()
