
from webcrawler.postgres.populateDB import change_dict_key

class WebcrawlerPipeline(object):
    def process_item(self, item, spider):
        name = type(item).__name__
        change_dict_key(item, name)