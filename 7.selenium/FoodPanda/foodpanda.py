import csv
import time
import datetime
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

prefs = {"profile.default_content_setting_values.notifications" : 2}

# open the browser with options
# print("===\nopen the browser\n===\n\n\n")
chrome_options = Options()
# chrome_options.add_argument('--dns-prefetch-disable')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--lang=en-US')
# chrome_options.add_argument('--headless')

# 停用瀏覽器上的顯示提醒 Notification 功能
chrome_options.add_argument("--disable-notifications")
# 視窗最大化
# chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome('assets/chromedriver.exe', chrome_options=chrome_options)

urls = []
city_names = []
data = {}

def get_food_pandas_restaurant(url):
   html = requests.get(url, headers={"connections":"close"})
   bs_text = BeautifulSoup(html.text, "lxml")
   all_li = []
   for k in bs_text.findAll("div", {"class":"dish-category-header"}):
       type_name = k.text.strip().split("\n")[0]
       try:
           type_note = k.text.strip().split("\n")[1:]
       except:
           type_note = []
       info = {
           "type_name":type_name,
           "type_note":type_note,
           "food":[]
       }
       all_li.append(info)
   cusine_list = bs_text.findAll("ul", {"class":"dish-list"})
   for num in range(len(all_li)):
       food_li = cusine_list[num]
       food_li = food_li.findAll("li")
       for food_text in food_li:
           food_text = food_text.text.strip().replace("\n","").replace(" ","").replace("Add","").split("NT$")
           try:
               food_name = food_text[0]
           except:
               food_name = ""
           try:
               food_price = food_text[1]
           except:
               food_price = ""
           all_li[num]["food"].append({"food_name":food_name,"food_price":food_price})
   return all_li

def parse_food_pandas_menu(html_data):
    if len(html_data)==0:
        return ""
    bs_text = BeautifulSoup(html_data, "lxml")
    all_li = []
    for k in bs_text.findAll("div", {"class":"dish-category-header"}):
        type_name = k.text.strip().split("\n")[0]
        try:
            type_note = k.text.strip().split("\n")[1:]
        except:
            type_note = []
        info = {
            "type_name":type_name,
            "type_note":type_note,
            "food":[]
        }
        all_li.append(info)
    cusine_list = bs_text.findAll("ul", {"class":"dish-list"})
    for num in range(len(all_li)):
        food_li = cusine_list[num]
        food_li = food_li.findAll("li")
        for food_text in food_li:
            food_text = food_text.text.strip().replace("\n","").replace(" ","").replace("Add","").split("NT$")
            try:
                food_name = food_text[0]
            except:
                food_name = ""
            try:
                food_price = food_text[1]
            except:
                food_price = ""
            all_li[num]["food"].append({"food_name":food_name,"food_price":food_price})
    return all_li

# driver = webdriver.Chrome()
# tw.tsv contains list of lists and every item in list have City name on [0] element and URL to city for ubereats on [1] element position
# This is a tab separated file
# e.g., Taipei  https://www.foodpanda.com.tw/city/taipei-city
with open('tw.tsv') as tsvfile:
    for item in tsvfile:
        urls.append(item.split('\t')[1].strip('\n').strip())
        city_names.append(item.split('\t')[0].strip())
        data[item.split('\t')[0].strip()] = []

for index, url in enumerate(urls):
    while 1:
        try:
            driver.get(url)
            break
        except:
            continue
    try:
        title = driver.find_element_by_css_selector('div.hero-section-text > p').text
    except:
        data[city_names[index]] = 'No Data Availabe'
        continue
    # if 'not found' in title.lower():
    if len(title.lower())==0:
        data[city_names[index]] = 'Page Not Found'
        continue
    restaurant_url = driver.find_elements_by_css_selector('div.restaurants__list > section > ul > li a')
    lenOfPage = driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    current_position = 1000
    res_uri = []

    # for i in restaurant_url:
    for i in restaurant_url[:1]:
        res_uri.append(i.get_attribute('href'))
    
    ############### Auto Scroll #######################
    while current_position < lenOfPage:
        driver.execute_script("window.scrollTo(0, " + str(current_position)+ ")")
        restaurant_url = driver.find_elements_by_css_selector('div.restaurants__list > section > ul > li a')
        time.sleep(5)
        for j in restaurant_url:
            try:
                res_uri.append(j.get_attribute('href'))
            except:
                pass
        current_position = current_position + 1000
    ############### Auto Scroll #######################

    resurl = set(res_uri)
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print(len(resurl))
    print('---------')
    print(city_names[index])
    if len(resurl) == 0:
        data[city_names[index]] = 'No Data Availabe'
        continue
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    for res_count, k in enumerate(resurl):
        # print('================================')
        # print(res_count)
        while 1:
            try:
                driver.get(k)
                break
            except:
                continue
        
        try:
            html_data = driver.page_source
            # soup = BeautifulSoup(html_data, "lxml")
            restaurant_name = driver.find_element_by_xpath('//div[contains(@class,"vendor-info-main-headline")]//h1').text
            cuisine_name = driver.find_element_by_xpath('//div[contains(@class,"vendor-info-main-details-cuisines")]').text
            cuisine_name = " ".join(cuisine_name.strip('$').strip().split('•'))
            cuisine_name = cuisine_name.replace("\n"," ").replace("$","").strip()
            rating = 0
            try:
                rating = driver.find_element_by_xpath('//span[contains(@class,"rating")]//strong').text
            except Exception as e:
                rating = 0
                pass
            
            actual_subcat = {}
            print(restaurant_name, cuisine_name, rating)
            actual_subcat = parse_food_pandas_menu(html_data)
            data[city_names[index]].append({'Restaurant Name': restaurant_name, 'Cuisine Type(s)': cuisine_name.strip('$').strip().split('•'), 'rating':rating, 'Menu': actual_subcat})
            restaurant_name = ""
            cuisine_name = ""
            actual_subcat = ""
            rating = ""
        except Exception as e:
            pass

    print('==============================================================')

today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(today[:10])
with open('output_'+today[:10]+'.json', 'w', encoding="utf-8") as fp:
    json.dump(data, fp)

print("Done.")