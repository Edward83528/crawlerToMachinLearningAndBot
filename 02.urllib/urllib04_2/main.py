#65001
import urllib.request
import time
import json

def start_requests():
    urls = [
        'https://www.mobile01.com/forumtopic.php?c=16&p=1',
        'https://www.mobile01.com/forumtopic.php?c=16&p=2',
    ]
    for url in urls:
        time.sleep(0.5) # 給個時間間隔,模擬人
        parseMobile01(url)

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
    items = []
    for a in html_data.split('c-listTableTd__title">')[1:]:
        link = 'https://www.mobile01.com/'+a.split('href="')[1].split('"')[0]
        title = a.split('c-link u-ellipsis" >')[1].split('</')[0]
        # print(title)
        # print(link)
        if len(title)>0 and len(link)>0:
            items.append([title, link])
    row_json = json.dumps(items, ensure_ascii=False) #json.dumps將 Python 對象編碼成 JSON 字符串
    print(row_json)

if __name__ == '__main__':
    start_requests()
    print("Done")