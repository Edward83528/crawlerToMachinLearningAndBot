#coding:utf-8
#65001
import urllib.request
import lxml.html

def start_requests():
    urls = [
        'https://www.mobile01.com/forumtopic.php?c=16&p=1',
    ]
    for url in urls:
        parseMobile01(url)

def parseMobile01(uri):
    title = ''
    link = ''
    
    handle = urllib.request.urlopen(uri)
    encoding = handle.headers.get_content_charset()
    html_data =  handle.read().decode(encoding)
    selector = lxml.html.document_fromstring(html_data)
    newslist = selector.xpath('//*[@id="maincontent"]/div[6]/table/tbody/tr')
    for i in range(len(newslist)):
        str_idx = str(i+1)
        title_path = '//*[@id="maincontent"]/div[6]/table/tbody/tr['+str_idx+']/td[1]/span/a//text()'
        title = selector.xpath(title_path)
        title = ''.join(title)
        link_path = '//*[@id="maincontent"]/div[6]/table/tbody/tr['+str_idx+']/td[1]/span/a//@href'
        link = selector.xpath(link_path)
        link = ''.join(link)
        link = 'https://www.mobile01.com/'+link
        print(title)
        print(link)
    

if __name__ == '__main__':
    start_requests();
    print("Done")