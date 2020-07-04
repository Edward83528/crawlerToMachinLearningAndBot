#coding:utf-8
#65001
import requests
from bs4 import BeautifulSoup

rs = requests.session()
res = rs.get('http://news.ltn.com.tw/search?keyword=川普&conditions=and&SYear=2018&SMonth=10&SDay=20&EYear=2018&EMonth=10&EDay=25&page=1')
html_data = res.text

# 以 Beautiful Soup 解析 HTML 程式碼
soup = BeautifulSoup(html_data, "lxml") #這裡用的是lxml解析器
for link in soup.find_all('a'): # 得到所有的a連結
    print(link.string) #取出連結文字
    print(link.get('href')) #取出href連結
    print('---'*30)