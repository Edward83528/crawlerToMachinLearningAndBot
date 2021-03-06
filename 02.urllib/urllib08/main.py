#coding:utf-8
#65001
import urllib.request
import json
import codecs
import sys
import argparse as ap
import time

# def argParse():
#     parser=ap.ArgumentParser(description='Mobile01 Crawler')
#     parser.add_argument("cid", help="Mobile01 Category ID")
#     parser.add_argument("pages", help="Pages")
#     return parser.parse_args()

# args=argParse()
# cid = args.cid
# pages = args.pages

cid = '27'
pages = '2'

def start_requests():
    urls = []
    for i in range(1,int(pages)+1):
        str_idx = ''+('%s' % i)
        urls.append('https://www.mobile01.com/forumtopic.php?c='+cid+'&p='+str_idx+'')

    for url in urls:
        print (url)
        parseMobile01(url)
        time.sleep(0.5) #時間間隔,模擬人

def parseMobile01(uri):
    req = urllib.request.Request(
        uri, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    handle = urllib.request.urlopen(req)
    # response得到的是網頁的内容，bytes類型的數據，需要用utf-8轉為字符串格式
    encoding = handle.headers.get_content_charset()
    html_data =  handle.read().decode(encoding)
    title = ''
    link = ''
    
    for a in html_data.split('l-listTable__td">')[1:]:
        if 'o-hashtag is-mini is-default' in a:
            # 公告
            link = 'https://www.mobile01.com/'+a.split('href="')[1].split('"')[0]
            title = a.split('c-link u-ellipsis" >')[1].split('</')[0]
        if 'o-hashtag is-mini is-heightLight' in a:
            # 置頂文
            link = 'https://www.mobile01.com/'+a.split('href="')[1].split('"')[0]
            title = a.split('c-link u-ellipsis" >')[1].split('</')[0]
        elif 'l-listTable__tbody' not in a:
            # 非置頂文, 中間有發現標頭的部分不處理
            link = 'https://www.mobile01.com/'+a.split('href="')[1].split('"')[0]
            title = a.split('c-link u-ellipsis" >')[1].split('</')[0]
        if len(title)>0 and len(link)>0:
            items.append([title, link])
        

if __name__ == '__main__':
    items = []
    start_requests();
    row_json = json.dumps(dict(items), ensure_ascii=False) #json.dumps將 Python 對象編碼成 JSON 字符串
    file = codecs.open('out.json', 'w', encoding='utf-8') # 用 codecs.open 寫入檔案
    file.write(row_json)
    file.close()
    print("Done")