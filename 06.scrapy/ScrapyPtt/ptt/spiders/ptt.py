import logging
import scrapy
from datetime import datetime
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
        # urls = ('https://www.ptt.cc/bbs/'+self.b+'/search?q=kkbox', )
        for url in urls:
            yield scrapy.Request(url,cookies={'over18':'1'}, callback=self.parse, headers=self.headers)


    def parse(self, response):
        self._pages += 1
        for href in response.css('.r-ent > div.title > a::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_post, headers=self.headers)
            
        if self._pages < PttCrawler.MAX_PAGES:
            next_page = response.xpath('//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
            if next_page:
                url = response.urljoin(next_page[0].extract())
                logging.warning('follow {}'.format(url))
                yield scrapy.Request(url, callback=self.parse , headers=self.headers)
            else:
                logging.warning('no next page')
        else:
            logging.warning('max pages reached')

        
    def parse_post(self, response):
        item = PttItem()

        item['board'] = self.b
        try:
            item['title'] = response.xpath('//div[@class="article-metaline"]/span[text()="標題"]/following-sibling::span[1]/text()')[0].extract()
            item['author'] = response.xpath('//div[@class="article-metaline"]/span[text()="作者"]/following-sibling::span[1]/text()')[0].extract().split(' ')[0]
            item['content'] = response.xpath('//div[@id="main-content"]/text()')[0].extract()
            datetime_str = response.xpath('//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span[1]/text()')[0].extract()
            if(len(datetime_str)!=24):
                datetime_str +=" "+str(datetime.datetime.now().year)
            item['date'] = datetime.datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y')
            #item['date'] = str(datetime.datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y'))
            #                                     main-content > span:nth-child(5)
            item['ip'] = response.xpath('//div[@id="main-content"]/span[contains(text(),"發信站: 批踢踢實業坊(ptt.cc)")]/text()')[0].extract().rstrip().split(' ')[-2:][0]
            item['locale'] = response.xpath('//div[@id="main-content"]/span[contains(text(),"發信站: 批踢踢實業坊(ptt.cc)")]/text()')[0].extract().rstrip().split(' ')[-1:][0]

            comments = []
            total_score = 0
            for comment in response.xpath('//div[@class="push"]'):
                push_tag = comment.css('span.push-tag::text')[0].extract()
                push_user = comment.css('span.push-userid::text')[0].extract()
                push_content = comment.css('span.push-content::text')[0].extract()
                #140.112.235.146 06/16 16:23
                # push_tmp = comment.css('span.push-ipdatetime::text')[0].extract()
                push_time = comment.css('span.push-ipdatetime::text')[0].extract().strip()
                # print(push_tmp)
                # push_tmp = push_tmp.strip()
                # push_ip = push_tmp.split(' ')[0]
                # push_time = push_tmp.split(' ')[1]+" "+push_tmp.split(' ')[2]

                if '推' in push_tag:
                    score = 1
                elif '噓' in push_tag:
                    score = -1
                else:
                    score = 0

                total_score += score
                comments.append({'user': push_user,
                                 'content': push_content,
                                 'score': score,
                                 # 'ip':push_ip,
                                 'time':push_time})

            item['comments'] = comments
            item['score'] = total_score
            item['url'] = response.url
            item['updatetime'] = datetime.datetime.now()
            #item['updatetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                print ( "%s  %-4s %-14s %s" % (item['date'],item['score'],item['author'],item['title']) )
            except Exception as e:
                print(str(e))
                pass
            yield item
        except Exception as e:
            print("Exception:"+str(e))
            print("======"+response.url+"======")
            pass
        
        
    
        self.log('HTML %s loaded' % response.url)