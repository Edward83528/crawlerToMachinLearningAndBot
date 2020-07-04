## 本專案大意  
    >>機器學習與深度學習NLP步驟如下:
    >資料蒐集(爬蟲) -> 資料清理 -> 特徵工程 -> NLP建模 -> 寫成API放到server
    >本專案會帶你從頭了解到NLP建模型
    >因為爬蟲非常依賴html元素與元素class和id的設定，所以爬蟲的那個網頁如果元素有換名稱，爬蟲程式就會爬不到嚕，所以商業上通常如果爬不到了，會做處理寄封信通知，然後趕緊修復
## 本專案python爬蟲實戰說明
| 單元 | 說明 | 快速連結 |
| :-----| :---- | :----: |
| 01.python_review | 如果您還對python不是那麼熟悉，本單元可讓您迅速學會基本python | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/01.python_review "python_review") |
| 02.urllib | 使用python自帶方法urllib | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/02.urllib "urllib") |
| 03.request | 使用第三方套件request爬蟲 | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/03.request "request") |
| 04.beautifulSoup | 開始使用beautifulSoup解析 | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/04.beautifulSoup "beautifulSoup") |
| 05.mongo | 介紹mongo DB如何使用 | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/05.mongo "mongo") |
| 06.scrapy | scrapy實戰 | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/06.scrapy "scrapy") |
| 07.selenium | selenium自動化實戰 | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/07.selenium "selenium") |
| 08.ptt_crawler | 爬PPT | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/08.ptt_crawler "ptt_crawler") |
| 09.php_crawler_articles | php爬蟲即時篇 | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/09.php_crawler_articles "php_crawler_articles") |
| 10.facebook-crawler | 爬facebook | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/10.facebook-crawler "facebook-crawler") |
| 11.linebot | linebot實戰 | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/11.linebot "linebot") |
| 12.MachineLearning | 爬蟲的資料應用在機器學習 | [連結](https://github.com/harry83528/crawlerToMachinLearningAndBot/tree/master/12.MachineLearning "MachineLearning") |


    >>判斷xpath
    > 1.   適合-table、有定義div、span
    > 2.   不適合-橫向排版、左右排列(才用split())
    > 3.   當然你也可以直接用beautifulSoup做解析
    
