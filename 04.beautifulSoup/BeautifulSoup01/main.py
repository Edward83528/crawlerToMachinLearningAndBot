#coding:utf-8
#65001
import requests
from bs4 import BeautifulSoup

rs = requests.session()
res = rs.get('http://news.ltn.com.tw/search?keyword=%E5%85%AB%E4%BB%99%E5%A1%B5%E7%88%86&conditions=and&SYear=2015&SMonth=6&SDay=27&EYear=2015&EMonth=8&EDay=24&page=1')
html_data = res.text

soup = BeautifulSoup(html_data, "lxml")
for link in soup.find_all('a'):
    print(link.get('href'))
