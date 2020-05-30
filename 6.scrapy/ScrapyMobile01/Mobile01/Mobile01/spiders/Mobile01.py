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
            tmp = 'https://www.mobile01.com/forumtopic.php?c=%s&p=%s' % (c,str_idx) 
            urls.append(tmp.strip())

        for url in urls:
            print (url)
            time.sleep(1)
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
        item = Mobile01Item()
        #//*[@id="maincontent"]/div[7]/table/tbody/tr[1]
        str_xpath = '/html/body/div/main/div[1]/div/div/div/div[1]/div[7]/div/div[2]/div/div[2]/div'
        count = len(response.xpath(str_xpath))
        for i in range(1,count+1):
            str_idx = ''+('%s' % i)
            str_xpath = '/html/body/div/main/div[1]/div/div/div/div[1]/div[7]/div/div[2]/div/div[2]/div['+str_idx+']/div[1]/div/div[2]/a//text()'
            titleList = response.xpath(str_xpath).extract()
            strTitle = ''.join(titleList)
            if len(strTitle.strip())==0:
                str_xpath = '/html/body/div/main/div[1]/div/div/div/div[1]/div[7]/div/div[2]/div/div[2]/div['+str_idx+']/div[1]/div/div/a//text()'
                strTitle = response.xpath(str_xpath).extract()
                strTitle = ''.join(strTitle)
            str_xpath = '/html/body/div/main/div[1]/div/div/div/div[1]/div[7]/div/div[2]/div/div[2]/div['+str_idx+']/div[1]/div/div[2]/a//@href'
            urlList = response.xpath(str_xpath).extract()
            strUrl = ''.join(urlList)
            if len(strUrl.strip())==0:
                str_xpath = '/html/body/div/main/div[1]/div/div/div/div[1]/div[7]/div/div[2]/div/div[2]/div['+str_idx+']/div[1]/div/div/a//@href'
                urlList = response.xpath(str_xpath).extract()
                strUrl = ''.join(urlList)
                print("="*20)
                print(strUrl)
                print("="*20)
            strUrl = 'https://www.mobile01.com/'+strUrl

            item['title'] = strTitle
            item['link'] = strUrl
            yield item
        
        self.log('HTML %s loaded' % response.url)
