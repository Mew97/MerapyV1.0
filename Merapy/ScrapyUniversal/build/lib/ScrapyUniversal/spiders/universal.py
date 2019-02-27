from scrapy.spiders import CrawlSpider
from ScrapyUniversal.items import UniversalItem
from ScrapyUniversal.loaders import UniversalLoader
from ScrapyUniversal.rules import rules
from ScrapyUniversal.custom_settings import SPIDER, START_URS, ALLOWED_DOMAINS, ITEM


class UniversalSpider(CrawlSpider):
    name = SPIDER
    start_urls = START_URS
    allowed_domains = ALLOWED_DOMAINS

    rules = rules

    def parse_start_url(self, response):
        loader = UniversalLoader(item=UniversalItem(), response=response)
        for key, value in ITEM.items():
            if value.get('method') == 'xpath':
                loader.add_xpath(key, value.get('args'), **{'re': value.get('re')})
            if value.get('method') == 'css':
                loader.add_css(key, value.get('args'), **{'re': value.get('re')})
            if value.get('method') == 'value':
                loader.add_value(key, value.get('args'), **{'re': value.get('re')})
            if value.get('method') == 'attr':
                loader.add_value(key, getattr(response, value.get('args')))
        yield loader.load_item()

    def parse_item(self, response):
        loader = UniversalLoader(item=UniversalItem(), response=response)
        for key, value in ITEM.items():
            if value.get('method') == 'xpath':
                loader.add_xpath(key, value.get('args'), **{'re': value.get('re')})
            if value.get('method') == 'css':
                loader.add_css(key, value.get('args'), **{'re': value.get('re')},)
            if value.get('method') == 'value':
                loader.add_value(key, value.get('args'), **{'re': value.get('re')})
            if value.get('method') == 'attr':
                loader.add_value(key, getattr(response, value.get('args')))
        yield loader.load_item()


