from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
 
# available since 2.4.0
from selenium.webdriver.support.ui import WebDriverWait
 
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC


# open the browser
print("===\nopen the browser\n===\n\n\n")
browser = webdriver.Chrome('assets/chromedriver.exe')
# makes sure slower connections work as well        
print ("Waiting 10 sec")
browser.implicitly_wait(10)

