import scrapy
import time
from urllib.parse import quote
from LTNSearch.items import LtnsearchItem

class LTNSearch(scrapy.Spider):
    name = "LTNSearch"
    #scrapy crawl LTNSearch -a k=八仙塵爆 -a s=2015-06-27 -a e=2015-08-24 -a p=2
    def __init__(self, k='', s='', e='', p='1', *args, **kwargs):
        super(LTNSearch, self).__init__(*args, **kwargs)
        self.k = k
        self.s = s
        self.e = e
        self.p = p
        
    def start_requests(self):
        start_date = self.s
        end_date = self.e
        keyword = self.k
        if( len(start_date.split("-"))==3 and len(end_date.split("-"))==3) :
            SYear = start_date.split("-")[0]
            SMonth = start_date.split("-")[1]
            SDay = start_date.split("-")[2]
            EYear = end_date.split("-")[0]
            EMonth = end_date.split("-")[1]
            EDay = end_date.split("-")[2]
            urls = []
            for i in range(1,int(self.p)+1):
                str_page = ''+('%s' % i)
                api = "https://news.ltn.com.tw/search?keyword={}&conditions=and&start_time={}&end_time={}&page={}".format(quote(keyword), start_date, end_date, str_page)
                urls.append(api)
            for url in urls:
                print (url)
                time.sleep(1)
                yield scrapy.Request(url=url, callback=self.parse)
        else:
          print('==================  date format error, ex:2015-06-27  ==================')


    def parse(self, response):
        item = LtnsearchItem()
        str_xpath = '//*[@class="searchlist boxTitle"]/li'
        count = len(response.xpath(str_xpath))
        for i in range(1,count+1):
            str_idx = ''+('%s' % i)
            str_xpath = '//*[@class="searchlist boxTitle"]/li['+str_idx+']/a//text()'
            titleList = response.xpath(str_xpath).extract()
            strTitle = ''.join(titleList)
            str_xpath = '//*[@class="searchlist boxTitle"]/li['+str_idx+']/a//@href'
            urlList = response.xpath(str_xpath)[0].extract()
            strUrl = ''.join(urlList)
            strUrl = strUrl
            str_xpath = '//*[@class="searchlist boxTitle"]/li['+str_idx+']/p//text()'
            bodyList = response.xpath(str_xpath).extract()
            strBody = ''.join(bodyList)
            str_xpath = '//*[@class="searchlist boxTitle"]/li['+str_idx+']/span//text()'
            dateList = response.xpath(str_xpath).extract()
            strDate = ''.join(dateList).replace("&nbsp;","")[:10]
            item['title'] = strTitle
            item['link'] = strUrl
            item['body'] = strBody
            item['postdate'] = strDate
            yield item

        
        self.log('HTML %s loaded' % response.url)
