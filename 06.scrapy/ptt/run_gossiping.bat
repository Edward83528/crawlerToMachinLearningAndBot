:loop
chcp 65001
scrapy crawl ptt -a b=Gossiping -a p=100000

timeout /t 600 /nobreak
goto :loop