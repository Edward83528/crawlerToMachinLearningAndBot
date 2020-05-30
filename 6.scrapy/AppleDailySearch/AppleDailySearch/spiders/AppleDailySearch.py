import scrapy
import time
import json

from AppleDailySearch.items import AppledailysearchItem
from bs4 import BeautifulSoup as bs
from urllib.parse import quote

class AppleDailySearch(scrapy.Spider):
    name = "AppleDailySearch"
    #scrapy crawl AppleDailySearch -a k=川普 -a s=2018-07-01 -a e=2018-07-19 -a p=2
    def __init__(self, k='', s='', e='', p='1', *args, **kwargs):
        super(AppleDailySearch, self).__init__(*args, **kwargs)
        self.k = k
        self.s = s
        self.e = e
        self.p = p
        
    def start_requests(self):
      if( len(self.s.split("-"))==3 and len(self.e.split("-"))==3) :
          urls = []
          for i in range(1,int(self.p)+1):
              str_idx = ''+('%s' % i)
              uri = 'https://tw.appledaily.com/search/result?sort=time&searchType=all&dateStart='+self.s.replace('-','%2F')+'&dateEnd='+self.e.replace('-','%2F')+'&querystrS='+quote(self.k)+"&page="+str_idx
              #data = {"searchMode":"Adv","searchType":"text","querystrA":self.k,"select":"AND","source":"","sdate":self.s,"edate":self.e,"sorttype":"1","page":str_idx}
              time.sleep(0.5)
              #yield scrapy.FormRequest(url=uri,formdata=data,callback=self.parse_post)
              yield scrapy.Request(url=uri, callback=self.parse_post)
      else:
          print('==================  date format error, ex:2018-12-01  ==================')

    def parse_post(self, response):
        str_xpath = '//*[@id="result"]/li'
        count = len(response.xpath(str_xpath))
        for i in range(1,count+1):
            str_idx = ''+('%s' % i)
            titleList = response.xpath('//*[@id="result"]/li['+str_idx+']/div/h2/a//text()').extract()
            strTitle = ''.join(titleList)
            strTitle = strTitle.strip()
            urlList = response.xpath('//*[@id="result"]/li['+str_idx+']/div/h2/a//@href')[0].extract()
            strUri = ''.join(urlList)
            dateList = response.xpath('//*[@id="result"]/li['+str_idx+']/div/time//text()').extract()
            strDate = ''.join(dateList)
            yield scrapy.Request(url=strUri, meta={'strTitle':strTitle, 'strUri':strUri, 'strDate':strDate}, callback=self.parse)

    def parse(self, response):
        item = AppledailysearchItem()
        strBody = ''
        html_data2 = response.body.decode('utf-8')
        soup2 = bs(html_data2,'html.parser')
        body_tmp = ''
        for p_soup2 in soup2.findAll('div',attrs={"class":"ndArticle_margin"}):
            body_tmp = p_soup2.getText().split('googletag')[0].replace('有話要說 投稿「即時論壇」','').split('.ndgKeyword')[0].split('，版權所有')[0].split('本新聞文字')[0].strip()
            if 'confirmOMOAdvFlag' in body_tmp:
                body_tmp = body_tmp.split('if')[0]
        if len(body_tmp)==0:
            try:
                tmp = (html_data2.split('Fusion.globalContent=')[1].split('promo_items')[0]+"}").split(',"}')[0]+"}"
                for k, v in enumerate(json.loads(tmp)["content_elements"]):
                    if k==0:
                        if 'content' in v:
                            body_tmp = v['content'] 
                    elif k==1:
                        if 'content' in v:
                            body_tmp = v['content'] 
            except Exception as e:
                pass
        strBody = body_tmp
        postdate = response.meta['strDate']
        item['title'] = response.meta['strTitle']
        item['link'] = response.meta['strUri']
        item['body'] = strBody
        item['postdate'] = postdate[0:4]+'-'+postdate[4:6]+'-'+postdate[6:8]
        yield item

        
        self.log('HTML %s loaded' % response.url)
