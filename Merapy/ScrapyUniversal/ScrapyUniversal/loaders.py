from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose


class Loader(ItemLoader):
    # default_output_processor = Compose(lambda s: s.strip())
    pass


class UniversalLoader(Loader):
    # text_out = Compose(Join(), lambda s: s.strip())
    # source_out = Compose(Join(), lambda s: s.strip())
    pass
