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
from bs4 import BeautifulSoup as bs
from urllib.parse import quote

#python main.py 八仙塵爆 2015-06-27 2015-08-24 1
#def argParse():
#    parser=ap.ArgumentParser(description='Liberty Time Net Crawler')
#    parser.add_argument("keyword", help="Serch Keyword")
#    parser.add_argument("start_date", help="Start (2017-01-01)")
#    parser.add_argument("end_date", help="End (2017-01-02)")
#    parser.add_argument("pages", help="Pages")
#    return parser.parse_args()

#args=argParse()
#keyword = quote(args.keyword)
#start_date = args.start_date
#end_date = args.end_date
#pages = args.pages

keyword = quote('八仙塵爆')
start_date = '2015-06-27'
end_date = '2015-08-24'
pages = '1'

def start_requests():
    if( len(start_date.split("-"))==3 and len(end_date.split("-"))==3) :
        SYear = start_date.split("-")[0]
        SMonth = start_date.split("-")[1]
        SDay = start_date.split("-")[2]
        EYear = end_date.split("-")[0]
        EMonth = end_date.split("-")[1]
        EDay = end_date.split("-")[2]
        urls = []
        for i in range(1,int(pages)+1):
            str_idx = ''+('%s' % i)
            urls.append('http://news.ltn.com.tw/search?keyword='+keyword+'&conditions=and&SYear='+SYear+'&SMonth='+SMonth+'&SDay='+SDay+'&EYear='+EYear+'&EMonth='+EMonth+'&EDay='+EDay+'&page='+str_idx+'')

        for url in urls:
            print (url)
            parseLtnNews(url)
            time.sleep(0.5)
    else:
        print ("Data format error.")

        
def request_uri(uri):
    header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    rs = requests.session()
    res = rs.get(uri, headers=header)
    html_data =  res.text
    #r = requests.post(url=uri, headers={'Connection':'close'})
    return html_data


def parseLtnNews(uri):
    postdate = ""
    link = ""
    title = ""
    body = ""
    html_data =  request_uri(uri)
    soup = bs(html_data,'html.parser')
    for ul_soup in soup.findAll('ul',attrs={"id":"newslistul"}):
        for span_soup in ul_soup.findAll('span'):
            postdate = span_soup.string.replace("&nbsp;","")[:10]
        for li_soup in ul_soup.findAll('li'):
            p_list = li_soup.findAll('p')
            body=p_list[1].getText()
            items.append({"uri":uri,"body":body,"updatetime":datetime.datetime.now().strftime('%Y-%m-%d')})
            #print({"uri":uri,"body":body,"updatetime":datetime.datetime.now().strftime('%Y-%m-%d')})
        for a_soup in ul_soup.findAll('a',attrs={"class":"tit"}):
            title = a_soup.getText()
            items.append({"uri":uri,"title":title,"updatetime":datetime.datetime.now().strftime('%Y-%m-%d')})
            #print(title)
        #TO DO

    
    

    

if __name__ == '__main__':
    items = []
    start_requests();
    row_json = json.dumps(items, ensure_ascii=False)
    file = codecs.open(urllib.parse.unquote(keyword)+'.json', 'w', encoding='utf-8')
    file.write(row_json)
    file.close()
  

    print("Done")