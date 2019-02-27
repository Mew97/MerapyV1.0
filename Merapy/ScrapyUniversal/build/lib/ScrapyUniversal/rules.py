from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = (
    
    Rule(LinkExtractor(restrict_xpaths='//div[@id=\'pageStyle\']//a[contains(., \'下一页\')]', ),
         callback='parse_item', follow=True, ),
    
)