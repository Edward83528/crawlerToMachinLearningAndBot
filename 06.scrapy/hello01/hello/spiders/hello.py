import scrapy

class PCHomeSpider(scrapy.Spider):
    name = "hello"

    def start_requests(self):
        urls = [
            'http://24h.pchome.com.tw/index/',
            #'http://ecshweb.pchome.com.tw/search/v3.3/all/results?q=Switch&page=1&sort=rnk/dc',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'pchome-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)