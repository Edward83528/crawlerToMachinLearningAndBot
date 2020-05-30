#!/usr/bin/env python
# -*- coding: utf-8 -*-
#65001
import requests

def request_uri(uri,name,password):
    html_data = ''
    try:
        header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
        data = {"name":name,"password":password}
        res = requests.post(uri, data=data, headers=header)
        html_data =  res.text
    except Exception as e:
        print(str(e))
        pass
    return html_data


def start_requests(uri,name,password):
    html_data =  request_uri(uri,name,password)
    print(html_data)


if __name__ == '__main__':
    start_requests('http://jumpin.cc/HelloForm/post.php','David','1234');
    print("Done")
