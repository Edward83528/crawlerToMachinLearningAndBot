#65001
import urllib.request
import json
import codecs

def start_requests():
    urls = [
        'https://www.mobile01.com/forumtopic.php?c=16&p=1',
    ]
    for url in urls:
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
    items = []   #to do 移到程式主進入點 以免覆蓋檔案
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
    row_json = json.dumps(dict(items), ensure_ascii=False) #json.dumps將 Python 對象編碼成 JSON 字符串
    #print(row_json)
    file = codecs.open('out.json', 'w', encoding='utf-8') # 用 codecs.open 寫入檔案
    file.write(row_json)
    file.close()

if __name__ == '__main__':
    start_requests();
    print("Done")