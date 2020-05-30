#coding:utf-8
#65001
import requests
import json
import codecs
import sys
import argparse as ap
import time
import pymongo as mg
import datetime
import lxml.html

# def argParse():
#     parser=ap.ArgumentParser(description='Mobile01 Crawler')
#     parser.add_argument("cid", help="Mobile01 Category ID")
#     parser.add_argument("pages", help="Pages")
#     return parser.parse_args()

# args=argParse()
# cid = args.cid
# pages = args.pages

cid = "27"
pages = "1"

rs = requests.session()
client = mg.MongoClient('127.0.0.1:27017')
db = client['mobile01']

def start_requests():
    urls = []
    for i in range(1,int(pages)+1):
        str_idx = ''+('%s' % i)
        urls.append('https://www.mobile01.com/forumtopic.php?c='+cid+'&p='+str_idx+'')

    for url in urls:
        print (url)
        parseMobile01(url)
        time.sleep(0.5)

def request_uri(uri):
    header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0)'}
    res = rs.get(uri, headers=header)
    html_data =  res.text
    return html_data

def parseMobile01(uri):
    html_data =  request_uri(uri)
    title = ''
    link = ''
    
    selector = lxml.html.document_fromstring(html_data)
    newslist = selector.xpath('/html/body/div/main/div[1]/div/div/div/div[1]/div[7]/div/div[2]/div/div[2]/div')
    for i in range(len(newslist)):
        str_idx = str(i+1)
        # 公告/置頂
        title_path = '/html/body/div/main/div[1]/div/div/div/div[1]/div[7]/div/div[2]/div/div[2]/div['+str_idx+']/div[1]/div/div[2]/a//text()'
        title = selector.xpath(title_path)
        title = ''.join(title)
        if len(title.strip())==0:
            title_path = '/html/body/div/main/div[1]/div/div/div/div[1]/div[7]/div/div[2]/div/div[2]/div['+str_idx+']/div[1]/div/div/a//text()'
            title = selector.xpath(title_path)
            title = ''.join(title)
        link_path = '/html/body/div/main/div[1]/div/div/div/div[1]/div[7]/div/div[2]/div/div[2]/div['+str_idx+']/div[1]/div/div[2]/a//@href'
        link = selector.xpath(link_path)
        link = ''.join(link)
        if len(link.strip())==0:
            link_path = '/html/body/div/main/div[1]/div/div/div/div[1]/div[7]/div/div[2]/div/div[2]/div['+str_idx+']/div[1]/div/div/a//@href'
            link = selector.xpath(link_path)
            link = ''.join(link)
        link = 'https://www.mobile01.com/'+link
        print(title)
        print(link)
        result = db.urllib.insert_one(
          {
              "title": title,
              "link":link,
              "datetime":datetime.datetime.now()
          })
        #items.append([title, link])

if __name__ == '__main__':
    start_requests();
    print("Done")