SPIDER = 'spider'

START_URS = ['http://tech.china.com/articles/', ]

ALLOWED_DOMAINS = ['tech.china.com']

COLLECTION = 'project112'

ITEM = {

    'title': {
        'method': 'xpath',
        'args': '//div[@class=\'conR\']/h2/a/text()',
        
    },

    'text': {
        'method': 'xpath',
        'args': '//div[@class=\'conR\']/div[@class=\'conR_txt\']/a/text()',
        
    },

}