import scrapy
import time

from AppleDailySearch.items import AppledailysearchItem
from bs4 import BeautifulSoup as bs

class AppleDailySearch(scrapy.Spider):
    name = "AppleDailySearch"
    #scrapy crawl AppleDailySearch -a k=八仙塵爆 -a s=2015-06-27 -a e=2015-08-24 -a p=2
    def __init__(self, k='', s='', e='', p='1', *args, **kwargs):
        super(AppleDailySearch, self).__init__(*args, **kwargs)
        self.k = k
        self.s = s
        self.e = e
        self.p = p
        
    def start_requests(self):
      if( len(self.s.split("-"))==3 and len(self.e.split("-"))==3) :
          uri = 'http://search.appledaily.com.tw/appledaily/search'
          urls = []
          for i in range(1,int(self.p)+1):
              str_idx = ''+('%s' % i)
              # TO DO
              
      else:
          print('==================  date format error, ex:2015-06-27  ==================')

    def parse_post(self, response):
        str_xpath = '//*[@id="result"]/li'
        count = len(response.xpath(str_xpath))
        for i in range(1,count+1):
            #TO DO

    def parse(self, response):
        item = AppledailysearchItem()
        #TO DO
        
        yield item

        
        self.log('HTML %s loaded' % response.url)
