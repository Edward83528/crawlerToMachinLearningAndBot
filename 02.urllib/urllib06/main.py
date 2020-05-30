#coding:utf-8
#65001
import urllib.request
import json
import codecs

def start_requests():
    urls = []
    for i in range(1,6):
        str_idx = ''+('%s' % i)
        urls.append('https://www.mobile01.com/forumtopic.php?c=16&p='+str_idx+'')

    for url in urls:
        print (url)
        parseMobile01(url)

def parseMobile01(uri):
    handle = urllib.request.urlopen(uri)
    encoding = handle.headers.get_content_charset()
    html_data =  handle.read().decode(encoding)
    title = ''
    link = ''
    items = []
    if len(html_data.split('class="subject"'))>1:
        for a in html_data.split('class="subject"')[1:]:
            if 'topic_top' in a:
                for b in a.split('class="topic_top" title="'):
                    title = b.split('">')[1].split('</a>')[0]
                    link = 'https://www.mobile01.com/'+b.split('href="')[1].split('">')[0]
            elif 'topic_gen' in a:
                for b in a.split('class="topic_gen" title="'):
                    title = b.split('">')[1].split('</a>')[0]
                    link = 'https://www.mobile01.com/'+b.split('href="')[1].split('">')[0]
            if (len(title)>0) and (len(link)>0):
                #print(title+'\n'+link)
                items.append([title, link])
        #row_json = json.dumps(items) 
        #print(row_json)
        row_json = json.dumps(dict(items), ensure_ascii=False)
        file = codecs.open('out.json', 'w', encoding='utf-8')
        file.write(row_json)
        file.close()

if __name__ == '__main__':
    start_requests();
    print("Done")