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

# def argParse():
#     parser=ap.ArgumentParser(description='Liberty Time Net Crawler')
#     parser.add_argument("keyword", help="Serch Keyword")
#     parser.add_argument("start_date", help="Start (2017-01-01)")
#     parser.add_argument("end_date", help="End (2017-01-02)")
#     parser.add_argument("pages", help="Pages")
#     return parser.parse_args()

# args=argParse()
# keyword = quote(args.keyword)
# start_date = args.start_date
# end_date = args.end_date
# pages = args.pages

keyword = quote('肺炎')
start_date = '2020-04-14'
end_date = '2020-04-15'
pages = '1'

def request_uri(uri):
    handle = urllib.request.urlopen(uri)
    encoding = handle.headers.get_content_charset()
    html_data =  handle.read().decode(encoding)
    return html_data

def strip_tags(html_data):
    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
    no_tags = tag_re.sub('', html_data)
    return re.sub('<[^<]+?>', '', html_data)

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
        #http://news.ltn.com.tw/search?keyword=蘋果&conditions=and&SYear=2018&SMonth=03&SDay=01&EYear=2018&EMonth=03&EDay=05&page=1
        api = 'http://news.ltn.com.tw/search?keyword='+keyword+'&conditions=and&SYear='+SYear+'&SMonth='+SMonth+'&SDay='+SDay+'&EYear='+EYear+'&EMonth='+EMonth+'&EDay='+EDay+'&page='+str_idx+''
        urls.append(api)
        print('http://news.ltn.com.tw/search?keyword='+keyword+'&conditions=and&SYear='+SYear+'&SMonth='+SMonth+'&SDay='+SDay+'&EYear='+EYear+'&EMonth='+EMonth+'&EDay='+EDay+'&page='+str_idx+'')
        for url in urls:
            #print (url)
            parseLtnNews(url)
            time.sleep(0.5)


def parseLtnNews(uri):
    handle = urllib.request.urlopen(uri)
    encoding = handle.headers.get_content_charset()
    html_data =  handle.read().decode(encoding)
    aryTemp01 = html_data.split('class="searchlist boxTitle"')
    if len(aryTemp01)>1:
        for a in aryTemp01[1].split('<li>'):
            title = ''
            link = ''
            body = ''
            postdate = ''
            aryTemp02 = a.split('<p>')
            if len(aryTemp02)>1:
                body = aryTemp02[1].split('</p>')[0].replace("\n","").replace("<strong>","").replace("</strong>","")
                #print(body)
            aryTemp02 = a.split('class="tit" href="')
            if len(aryTemp02)>1:
                title = aryTemp02[1].split('">')[1].split("</a>")[0].replace("\n","").replace("<strong>","").replace("</strong>","")
                print(title)
                aryTemp03 = aryTemp02[1].split('"')
                link = aryTemp03[0]
                print(link)
                html_data2 = request_uri(link)
                if 'data-desc="內文">' in html_data2:
                        aryTemp02 = html_data2.split('data-desc="內文">')
                        aryTemp03 = aryTemp02[1].split('</span>')
                        if len(aryTemp03)>1:
                            aryTemp04 = aryTemp03[1].split('<ul class="pic300')
                            #print(aryTemp04[0])
                            if len(aryTemp04)>1:
                                body = ''.join(aryTemp04[0].split('\n'))
                                body = ''.join(body.split('<p>'))
                                body = ''.join(body.split('</p>'))
                                body = ''.join(body.split('</b>'))
                            elif 'oneadIRTag' in aryTemp03[1]:
                                aryTemp04 = aryTemp03[1].split('<div id')
                                if len(aryTemp04)>1:
                                    body = ''.join(aryTemp04[0].split('\n'))
                                    body = ''.join(body.split('<p>'))
                                    body = ''.join(body.split('</p>'))
                                    body = ''.join(body.split('</b>'))
                                
                if(len(body)==0):
                    aryTemp02 = html_data2.split('articleBody">')
                    if len(aryTemp02)>2:
                        aryTemp03 = aryTemp02[2].split('class="ph_d">')
                        if len(aryTemp03)>1:
                            aryTemp04 = aryTemp03[1].split('</div>')
                            if len(aryTemp04)>1:
                                body = ''.join(aryTemp04[0].split('\n'))
                                body = ''.join(body.split('<p>'))
                                body = ''.join(body.split('</p>'))
                                body = ''.join(body.split('</b>'))
                                if '<table' in body:
                                    body = body.split('<table')[0]
                                body = body.replace('</span>','').replace('<span>','')
                                #print(body)
                            else:
                                #<p><span class="ph_b ph_d1">
                                aryTemp04 = aryTemp03[1].split('<p><span class="ph_b ph_d1">')
                                if len(aryTemp04)>1:
                                    body = ''.join(aryTemp04[0].split('\n'))
                                    body = ''.join(body.split('<p>'))
                                    body = ''.join(body.split('</p>'))
                                    body = ''.join(body.split('</b>'))
                                    if '<table' in body:
                                        body = body.split('<table')[0]
                                        body = body.replace('</span>','').replace('<span>','')
                        else:
                            aryTemp04 = aryTemp02[1].split('</div>')
                            if len(aryTemp04)>1:
                                body = ''.join(aryTemp04[0].split('\n'))
                                body = ''.join(body.split('<p>'))
                                body = ''.join(body.split('</p>'))
                                body = ''.join(body.split('</b>'))
                                if '<table' in body:
                                    body = body.split('<table')[0]
                                body = body.replace('</span>','').replace('<span>','')
                    elif len(aryTemp02)>1:
                        if "class='ph_d'" in aryTemp02[1]:
                            aryTemp03 = aryTemp02[1].split("class='ph_d'>")
                        elif 'class="ph_d"' in aryTemp02[1]:
                            aryTemp03 = aryTemp02[1].split('class="ph_d">')
                        if len(aryTemp03)>1:
                            aryTemp04 = aryTemp03[1].split('</div>')
                            if len(aryTemp04)>1:
                                body = ''.join(aryTemp04[0].split('\n'))
                                body = ''.join(body.split('<p>'))
                                body = ''.join(body.split('</p>'))
                                body = ''.join(body.split('</b>'))
                                if '<table' in body:
                                    body = body.split('<table')[0]
                                body = body.replace('</span>','').replace('<span>','')
                                #print(body)
                            else:
                                #<p><span class="ph_b ph_d1">
                                aryTemp04 = aryTemp03[1].split('<p><span class="ph_b ph_d1">')
                                if len(aryTemp04)>1:
                                    body = ''.join(aryTemp04[0].split('\n'))
                                    body = ''.join(body.split('<p>'))
                                    body = ''.join(body.split('</p>'))
                                    body = ''.join(body.split('</b>'))
                                    if '<table' in body:
                                        body = body.split('<table')[0]
                                        body = body.replace('</span>','').replace('<span>','')
                        else:
                            aryTemp04 = aryTemp02[1].split('</div>')
                            if len(aryTemp04)>1:
                                body = ''.join(aryTemp04[0].split('\n'))
                                body = ''.join(body.split('<p>'))
                                body = ''.join(body.split('</p>'))
                                body = ''.join(body.split('</b>'))
                                if '<table' in body:
                                    body = body.split('<table')[0]
                                body = body.replace('</span>','').replace('<span>','')
                                #print(body)
                body = body.split('<iframe')[0]
                body = body.split('<script>')[0]
                if(str(body)==''):
                    #re.sub('<[^<]+?>', '', text)
                    tmpBody = []
                    aryTemp02 = html_data2.split('articleBody">')
                    if len(aryTemp02)>1:
                        aryTemp03 = aryTemp02[1].split("<span class='ph_b'>")
                        if len(aryTemp03)>1:
                            for x in aryTemp03[1:]:
                                if 'div-inread-ad' in x:
                                    tmpBody.append(strip_tags(x.split('<div id="div-inread-ad">')[0]))
                                else:
                                    tmpBody.append(strip_tags(x))
                            body = ' '.join(tmpBody)
                    if(str(body)==''):
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