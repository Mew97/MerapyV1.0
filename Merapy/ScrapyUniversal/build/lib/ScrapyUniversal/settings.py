BOT_NAME = 'ScrapyUniversal'
SPIDER_MODULES = ['ScrapyUniversal.spiders']
NEWSPIDER_MODULE = 'ScrapyUniversal.spiders'
ROBOTSTXT_OBEY = False
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
LOG_LEVEL = 'WARNING'
SELENIUM_TIMEOUT = 20
PHANTOMJS_SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
DOWNLOAD_PATH = '/download/download/project112.txt'


DOWNLOADER_MIDDLEWARES = {
    'ScrapyUniversal.middlewares.SeleniumMiddleware': 543,
}


ITEM_PIPELINES = {
    
    'ScrapyUniversal.pipelines.MongoPipeline': 300,
    
}


ALICE_MONGO_URI = 'mongodb://zhubo:zb52971552@localhost:27017/admin'


MONGO_DB = 'zhubo00'
