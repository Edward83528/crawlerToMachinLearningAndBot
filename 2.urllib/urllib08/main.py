#coding:utf-8
#65001
import urllib.request
import json
import codecs
import sys
import argparse as ap
import time
import datetime
from urllib.parse import quote

def argParse():
    parser=ap.ArgumentParser(description='Liberty Time Net Crawler')
    parser.add_argument("keyword", help="Serch Keyword")
    parser.add_argument("start_date", help="Start (2017-01-01)")
    parser.add_argument("end_date", help="End (2017-01-02)")
    parser.add_argument("pages", help="Pages")
    return parser.parse_args()

args=argParse()
keyword = quote(args.keyword)
start_date = args.start_date
end_date = args.end_date
pages = args.pages

# keyword = quote('蘋果')
# start_date = '2017-11-20'
# end_date = '2017-11-21'
# pages = '2'

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
            time.sleep(0.5)


def parseLtnNews(uri):
    handle = urllib.request.urlopen(uri)
    encoding = handle.headers.get_content_charset()
    html_data =  handle.read().decode(encoding)
    aryTemp01 = html_data.split('class="searchlist">')
    if len(aryTemp01)>1:
        for a in aryTemp01[1].split('<li>'):
            title = ''
            link = ''
            body = ''
            postdate = ''
            aryTemp02 = a.split('<p>')
            if len(aryTemp02)>2:
                aryTemp03 = aryTemp02[1].split('</p>')
                title = aryTemp03[0].replace("<strong>","")
                print(title)
                aryTemp03 = aryTemp02[2].split('</p>')
                body = "".join(aryTemp03[0].split("\n")).replace("</strong>","")
                body = body.replace("<strong>","")
                print(body)
            aryTemp02 = a.split('class="tit" href="')
            if len(aryTemp02)>1:
                aryTemp03 = aryTemp02[1].split('"')
                link = "http://news.ltn.com.tw/"+aryTemp03[0]
                print(link)
            aryTemp02 = a.split('<span>')
            if len(aryTemp02)>1:
                postdate = aryTemp02[1].split('</span>')[0].replace("&nbsp;","")[:10]
                print(postdate)
            if len(title)>1:
                items.append({
                    "title": title,
                    "link":link,
                    "body":body,
                    "postdate":postdate,
                    #"updatetime":datetime.datetime.now(),  # MongoDB
                    "updatetime":datetime.datetime.now().strftime('%Y-%m-%d')
                    })
        

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