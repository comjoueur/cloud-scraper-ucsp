# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy import Spider


class BaseSpider(Spider):
    base_url = ""
    index = ""

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.base_url]
        self.es_index = self.index or self.name
