# coding=utf-8

import urllib.request
import json
import codecs
import datetime
import lxml.html
from urllib.parse import quote
from random import randint

from flask import Flask, render_template, request, make_response
from flask import jsonify

import sys
import time  
import hashlib
import threading
import datetime

def start_requests(keyword, start_date, end_date, pages="1"):
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
        api = "https://news.ltn.com.tw/search?keyword={}&conditions=and&start_time={}&end_time={}&page={}".format(quote(keyword), start_date, end_date, str_idx)
        urls.append(api)
        for url in urls:
            print (url)
            parseLtnNews(url)
            time.sleep(0.2)

def parseLtnNews(uri):
    print(uri)
    handle = urllib.request.urlopen(uri)
    encoding = handle.headers.get_content_charset()
    html_data =  handle.read().decode(encoding)
    selector = lxml.html.document_fromstring(html_data)
    newslist = selector.xpath('//*[@class="searchlist boxTitle"]/li')
    print(range(len(newslist)))
    for i in range(len(newslist)):
        strTitle = ''
        strUrl = ''
        strBody = ''
        strDate = ''
        str_idx = str(i+1)
        str_xpath = '//*[@class="searchlist boxTitle"]/li['+str_idx+']/a//text()'
        titleList = selector.xpath(str_xpath)
        strTitle = " ".join(titleList)
        print(strTitle)
        
        str_xpath = '//*[@class="searchlist boxTitle"]/li['+str_idx+']/a//@href'
        urlList = selector.xpath(str_xpath)[0]
        strUrl = ''.join(urlList)
        strUrl = strUrl
        print(strUrl)
        str_xpath = '//*[@class="searchlist boxTitle"]/li['+str_idx+']/p//text()'
        bodyList = selector.xpath(str_xpath)
        strBody = ''.join(bodyList).replace('\n','')
        str_xpath = '//*[@class="searchlist boxTitle"]/li['+str_idx+']/span//text()'
        dateList = selector.xpath(str_xpath)
        strDate = ''.join(dateList).replace("&nbsp;","")[:10]
        if len(strTitle)>1:
            items.append({
                "title": strTitle,
                "link":strUrl,
                "body":strBody,
                "postdate":strDate,
                #"updatetime":datetime.datetime.now(),  # MongoDB
                "updatetime":datetime.datetime.now().strftime('%Y-%m-%d')
                })
    handle.close()

def heartbeat():
    print (time.strftime('%Y-%m-%d %H:%M:%S - heartbeat', time.localtime(time.time())))
    timer = threading.Timer(60, heartbeat)
    timer.start()
timer = threading.Timer(60, heartbeat)
timer.start()

app = Flask(__name__,static_url_path="/static") 
@app.route('/message', methods=['POST'])

def reply():
    keyword = request.form['msg']
    res_msg = "Res:"
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterday = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')
    start_requests(keyword, yesterday, today, "1")
    rand_post_index = randint(0, len(items)-1)
    t = items[rand_post_index]["title"]
    l = "<a href='"+items[rand_post_index]["link"]+"'>"+items[rand_post_index]["link"]+"</a>"
    res_msg = t+"\n"+l
    if res_msg == ' ':
        res_msg = 'No Data input'

    return jsonify( { 'text': res_msg } )


"""
jsonify:是用於處理序列化json資料的function，就是將資料combine成json格式回傳

http://flask.pocoo.org/docs/0.12/api/#module-flask.json
"""


@app.route("/")
def index(): 
    return render_template("index.html")

#_________________________________________________________________

# 啟動APP
if (__name__ == "__main__"):
    items = []
    app.run(host = '127.0.0.1', port = 9999)
