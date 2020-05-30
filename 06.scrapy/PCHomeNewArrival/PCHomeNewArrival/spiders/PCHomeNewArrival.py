import scrapy
import json

from PCHomeNewArrival.items import PchomenewarrivalItem

class PCHomeNewArrival(scrapy.Spider):
    name = "PCHomeNewArrival"

    def start_requests(self):
        urls = [
            'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/replenish/prod&_callback=jsonpcb_replenish&431434',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_string = response.body.decode('utf-8').split("jsonpcb_replenish(")[1].split("]);")[0]+"]"
        json_data = json.loads(json_string)

        item = PchomenewarrivalItem()
        for json_array in json_data:
            item['title'] = json_array["Name"]
            item['link'] = "http://24h.pchome.com.tw/prod/"+json_array["Id"]
            #https://e.ecimg.tw/items/DYAL81A9009TIC8/000002_1550739451.jpg
            item['img'] = "https://e.ecimg.tw/"+json_array["Pic"]["S"]
            yield item

        print('\n')
        self.log('HTML %s loaded' % response.url)