#coding:utf-8

import urllib.request

if __name__ == '__main__':
    uri = "https://www.mobile01.com/forumtopic.php?c=16&p=1"
    #uri = 'https://tw.news.yahoo.com/weather'
    handle = urllib.request.urlopen(uri)
    encoding = handle.headers.get_content_charset()
    html_data =  handle.read().decode(encoding)
    print(html_data)
  