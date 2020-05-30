
# coding: utf-8

# # 查詢蘋果日報關鍵字搜尋，儲存至MongoDB

# In[3]:


#coding:utf-8
#65001
import urllib.request
import json
import codecs
import sys
import argparse as ap
import time
import datetime
import requests
import random
import pymongo as mg
from bs4 import BeautifulSoup as bs
from urllib.parse import quote

#python main.py 八仙塵爆 2015-06-27 2015-08-24 1
#def argParse():
#    parser=ap.ArgumentParser(description='Apple Daily News Crawler')
#    parser.add_argument("keyword", help="Serch Keyword")
#    parser.add_argument("start_date", help="Start (2017-01-01)")
#    parser.add_argument("end_date", help="End (2017-02-02)" )
#    parser.add_argument("pages", help="Pages")
#    return parser.parse_args()

#args=argParse()
#keyword = args.keyword
#start_date = args.start_date
#end_date = args.end_date
#pages = args.pages

keyword = '川普'
start_date = '2018-07-01'
end_date = '2018-07-19'
pages = '1'

client = mg.MongoClient('127.0.0.1:27017')
db = client['applenews']

rs = requests.session()

def start_requests(uri):
    if( len(start_date.split("-"))==3 and len(end_date.split("-"))==3) :
        for i in range(1,int(pages)+1):
            str_page = ''+('%s' % i)
            str_rand = str(random.randint(1,99999))
            print (uri+", page="+str_page)
            parseAppleDailyNews(uri+"&page="+str_page)
            time.sleep(0.5)
      
    else:
        print ("Data format error.")


def request_uri(uri,str_page):
    #header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0','Content-Type': 'application/x-www-form-urlencoded', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Encoding':'gzip, deflate','Referer':'http://search.appledaily.com.tw/appledaily/search'}
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
    data = {"searchMode":"Adv","searchType":"text","querystrA":keyword,"select":"AND","source":"","sdate":start_date,"edate":end_date,"sorttype":"1","page":str_page}
    res = rs.post(uri, data=data, headers=header)
    html_data =  res.text
    return html_data

                        
def request_uri_content(uri):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
    res = rs.get(uri, headers=header)
    html_data =  res.text
    return html_data


def parseAppleDailyNews(uri):
    # https://tw.appledaily.com/search/result?sort=time&searchType=all&dateStart=2018/07/01&dateEnd=2018/07/19&querystrS=川普&page=2
    html_data =  request_uri_content(uri)
    soup = bs(html_data,'html.parser')
    
    postdate = []
    link = []
    title = []
    body = []
    for div_soup in soup.findAll('div',attrs={"class":"content"}):
        #items.append({"uri":uri+'&page='+str_page,"div_soup":str(div_soup),"updatetime":datetime.datetime.now().strftime('%Y-%m-%d')})
        for a_soup in div_soup.findAll('h2'):
            tmp_title = a_soup.text
            title.append(tmp_title.strip())
        for p_soup in div_soup.findAll('p'):
            body.append(p_soup.text)
        for li_soup in div_soup.findAll('li'):
            for a_soup in li_soup.findAll('a'):
                content_uri = a_soup.get('href').strip()
                link.append(content_uri)
                print(content_uri)
                html_data2 = request_uri_content(content_uri)
                soup2 = bs(html_data2,'html.parser')
                body_tmp = ''
                if len(soup2.findAll('div',attrs={"class":"ndArticle_margin"}))==0:
                    body.append('N/A')
                else:
                    for p_soup2 in soup2.findAll('div',attrs={"class":"ndArticle_margin"}):
                        body_tmp = p_soup2.getText().split('googletag')[0].replace('有話要說 投稿「即時論壇」','').split('.ndgKeyword')[0].strip()
                        if 'confirmOMOAdvFlag' in body_tmp:
                            body_tmp = body_tmp.split('if')[0]
                        print(body_tmp)
                        body.append(body_tmp)
#                 time.sleep(0.5)

    for time_soup in soup.findAll('time'):
        tmp_d = ''
        if len(time_soup.getText())==8:
            tmp_d = time_soup.getText()[0:4]+'-'+time_soup.getText()[4:6]+'-'+time_soup.getText()[6:8]
        #elif len(time_soup.getText())==5:
            #tmp_d = datetime.datetime.now().strftime('%Y-%m-%d')
        if len(tmp_d)>1:
            postdate.append(tmp_d)
    
    current = 0
    while current < len(postdate):
        result = db.urllib.insert_one({
                "title": title[current],
                "link":link[current],
                "body":body[current],
                "postdate":postdate[current],
                "datetime":datetime.datetime.now(),
                "updatetime":datetime.datetime.now().strftime('%Y-%m-%d')
            })
        current+=1




if __name__ == '__main__':
    uri = 'https://tw.appledaily.com/search/result?sort=time&searchType=all&dateStart='+start_date.replace('-','%2F')+'&dateEnd='+end_date.replace('-','%2F')+'&querystrS='+quote(keyword)
    items = []
    start_requests(uri);
    row_json = json.dumps(items, ensure_ascii=False)
    file = codecs.open(urllib.parse.unquote(keyword)+'.json', 'w', encoding='utf-8')
    file.write(row_json)
    file.close()
    r = requests.get(url=uri, headers={'Connection':'close'})

    print("Done")

