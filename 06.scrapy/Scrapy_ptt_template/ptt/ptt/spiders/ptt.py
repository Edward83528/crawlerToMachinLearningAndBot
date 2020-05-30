import logging
import scrapy
import datetime

from ptt.items import PttItem

class PttCrawler(scrapy.Spider):
    name = "ptt"
    allowed_domains = ['ptt.cc']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    
    _pages = 0
    MAX_PAGES = 10
    
    #scrapy crawl ptt -a b=Gossiping -a p=2
    def __init__(self, b='', p='1', *args, **kwargs):
        super(PttCrawler, self).__init__(*args, **kwargs)
        self.b = b
        PttCrawler.MAX_PAGES = int(p)


    def start_requests(self):
        urls = ('https://www.ptt.cc/bbs/'+self.b+'/index.html', )
        for url in urls:
            yield scrapy.Request(url,cookies={'over18':'1'}, callback=self.parse, headers=self.headers)


    def parse(self, response):
        self._pages += 1
        for href in response.css('.r-ent > div.title > a::attr(href)'):
            print(href)
        
        item = PttItem()
        
        item['board'] = self.b
        item['title'] = ''
        item['author'] = ''
        item['content'] = ''
        item['date'] = ''
        item['ip'] = ''
        item['comments'] = ''
        item['score'] = ''
        item['url']=response.url
        item['datetime'] = datetime.datetime.now()
        yield item
            
        self.log('HTML %s loaded' % response.url)