
# coding: utf-8

# # 查詢自由時報關鍵字，儲存至MongoDB

# In[1]:


#coding:utf-8
#65001
import urllib.request
import json
import codecs
import sys
import argparse as ap
import time
import datetime
import lxml.html
import pymongo as mg
from urllib.parse import quote

#python main.py 世大運 2015-07-01 2017-07-03 1
# def argParse():
#     parser=ap.ArgumentParser(description='Liberty Time Net Crawler')
#     parser.add_argument("keyword", help="Serch Keyword")
#     parser.add_argument("start_date", help="Start (2017-01-01)")
#     parser.add_argument("end_date", help="End (2017-01-02)")
#     parser.add_argument("pages", help="Pages")
#     return parser.parse_args()

# args=argParse()
# keyword = quote(args.keyword)
# start_date = args.start_date
# end_date = args.end_date
# pages = args.pages

keyword = quote('川普')
start_date = '2018-07-01'
end_date = '2018-07-19'
pages = '1'

client = mg.MongoClient('127.0.0.1:27017')
db = client['ltnews']

def start_requests():
    start_list = start_date.split("-")
    end_list = end_date.split("-")
    SYear = ''
    SMonth = ''
    SDay = ''
    EYear = ''
    EMonth = ''
    EDay = ''
    if(len(start_list)==3) and (len(end_list)==3):
        SYear = start_list[0]
        SMonth = start_list[1]
        SDay = start_list[2]
        EYear = end_list[0]
        EMonth = end_list[1]
        EDay = end_list[2]
    else:
        print ("Date format error.")
  
    urls = []
    for i in range(1,int(pages)+1):
        str_idx = ''+('%s' % i)
        #http://news.ltn.com.tw/search?keyword=世大運&conditions=and&SYear=2015&SMonth=6&SDay=27&EYear=2015&EMonth=8&EDay=24&page=1
        urls.append('http://news.ltn.com.tw/search?keyword='+keyword+'&conditions=and&SYear='+SYear+'&SMonth='+SMonth+'&SDay='+SDay+'&EYear='+EYear+'&EMonth='+EMonth+'&EDay='+EDay+'&page='+str_idx+'')
        for url in urls:
            #print (url)
            parseLtnNews(url)
            time.sleep(0.2)


def parseLtnNews(uri):
    handle = urllib.request.urlopen(uri)
    encoding = handle.headers.get_content_charset()
    html_data =  handle.read().decode(encoding)
    selector = lxml.html.document_fromstring(html_data)
    newslist = selector.xpath('//*[@id="newslistul"]/li')
    print(str(len(newslist)))
    for i in range(len(newslist)):
        strTitle = ''
        strUrl = ''
        strBody = ''
        strDate = ''
        str_idx = str(i+1)
        str_xpath = '//*[@id="newslistul"]/li['+str_idx+']/a[2]/p//text()'
        titleList = selector.xpath(str_xpath)
        strTitle = " ".join(titleList)
        print(strTitle)
        str_xpath = '//*[@id="newslistul"]/li['+str_idx+']/a//@href'
        urlList = selector.xpath(str_xpath)[0]
        strUrl = ''.join(urlList)
        strUrl = 'http://news.ltn.com.tw'+strUrl
        str_xpath = '//*[@id="newslistul"]/li['+str_idx+']/p//text()'
        bodyList = selector.xpath(str_xpath)
        strBody = ''.join(bodyList).replace('\n','')
        str_xpath = '//*[@id="newslistul"]/li['+str_idx+']/span//text()'
        dateList = selector.xpath(str_xpath)
        strDate = ''.join(dateList).replace("&nbsp;","")[:10]
        if len(strTitle)>1:
            result = db.urllib.insert_one({
                "title": strTitle,
                "link":strUrl,
                "body":strBody,
                "postdate":strDate,
                "datetime":datetime.datetime.now(),
                "updatetime":datetime.datetime.now().strftime('%Y-%m-%d')
            })
    handle.close()



if __name__ == '__main__':
    items = []
    start_requests();
    row_json = json.dumps(items, ensure_ascii=False)
    file = codecs.open(urllib.parse.unquote(keyword)+'.json', 'w', encoding='utf-8')
    #file = codecs.open('out.json', 'w', encoding='utf-8')
    file.write(row_json)
    file.close()
    #print(row_json)
    print("Done")

