import scrapy
import time

from HelloScrapyPost.items import HelloscrapypostItem

class HelloScrapyPost(scrapy.Spider):
    name = "HelloScrapyPost"
    #scrapy crawl HelloScrapyPost -a n=David -a p=1234
    def __init__(self, n='', p='', *args, **kwargs):
        super(HelloScrapyPost, self).__init__(*args, **kwargs)
        self.n = n
        self.p = p
        
    def start_requests(self):
        uri = 'http://jumpin.cc/HelloForm/post.php'
        print (uri)
        data={'name': self.n, 'password': self.p}
        yield scrapy.FormRequest(url=uri,formdata=data,callback=self.parse_post)


    def parse_post(self, response):
        uri = 'http://jumpin.cc/HelloForm/content.php'
        print (uri)
        yield scrapy.Request(url=uri, callback=self.parse)


    def parse(self, response):
        item = HelloscrapypostItem()
        str_xpath = '/html/body//text()'
        body = response.xpath(str_xpath).extract()
        item['title'] = body
        item['link'] = ''+response.url
        yield item
        
        
        self.log('HTML %s loaded' % response.url)