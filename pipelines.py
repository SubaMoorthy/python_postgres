
from webcrawler.postgres.populateDB import change_dict_key

class WebcrawlerPipeline(object):
    def process_item(self, item, spider):
        # print('insde')
        name = type(item).__name__
        #print(name)
        #print(item)
        change_dict_key(item, name)