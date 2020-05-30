import scrapy
import time

from Mobile01.items import Mobile01Item
 
class Mobile01(scrapy.Spider):
    name = "Mobile01"
    #scrapy crawl Mobile01 -a c=16 -a p=1
    def __init__(self, c='16', p='1', *args, **kwargs):
        super(Mobile01, self).__init__(*args, **kwargs)
        self.c = c
        self.p = p
        
    def start_requests(self):
        urls = []
        c = self.c
        for i in range(1,int(self.p)+1):
            str_idx = ''+('%s' % i)
            tmp = '' # TO DO
            urls.append(tmp.strip())

        for url in urls:
            print (url)
            time.sleep(1)
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
        item = Mobile01Item()
        str_xpath = '/html/body/div/main/div[1]/div/div/div/div[1]/div[6]/div/div[2]/div/div[2]/div'
        count = len(response.xpath(str_xpath))
        for i in range(1,count+1):
            str_idx = ''+('%s' % i)
            # TO DO


            item['title'] = strTitle
            item['link'] = strUrl
            yield item
        
        self.log('HTML %s loaded' % response.url)
