import scrapy
import json
import datetime

from PCHomeSearch.items import PchomesearchItem

class PCHomeSearch(scrapy.Spider):
    name = "PCHomeSearch"

    #scrapy crawl PCHomeSearch -a k=iphone -a p=2
    def __init__(self, k='', p='1', *args, **kwargs):
        super(PCHomeSearch, self).__init__(*args, **kwargs)
        self.k = k
        self.p = p


    def start_requests(self):
        urls = []
        for i in range(1,int(self.p)+1):
            str_page = ''+('%s' % i)
            urls.append('http://ecshweb.pchome.com.tw/search/v3.3/all/results?q='+self.k+'&page='+str_page+'&sort=rnk/dc')
        
        for url in urls:
            print (url)
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        json_data = json.loads(response.body.decode('utf-8'))

        item = PchomesearchItem()
        for json_array in json_data["prods"]:
            item['title'] = json_array["name"]
            item['link'] = "http://24h.pchome.com.tw/prod/"+json_array["Id"]
            item['desc'] = json_array["describe"]
            item['price'] = json_array["price"]
            item['datetime'] = datetime.datetime.now()
            yield item
            
        print('\n')
        self.log('HTML %s loaded' % response.url)