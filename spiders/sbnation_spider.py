
import scrapy
from webcrawler.items import SBNationPlayer
class SbnationSpider(scrapy.Spider):
    name = 'sbnation'
    allowed_domains = ['sbnation.com']
    start_urls = ["http://www.sbnation.com/blogs#soccer"]

    def parse(self, response):
        teamlinks = response.xpath("//div[preceding-sibling::h2/@id='soccer' and following-sibling::h2/@id='combat-sports']/a/@href")
        for url in teamlinks:
            yield scrapy.Request(url.extract(), callback=self.parse)

        rosterlink = response.xpath("//a[substring(@href,string-length(@href)-6)='#roster']/@href")
        if len(rosterlink) > 0:
            yield scrapy.Request(rosterlink[0].extract(), callback=self.parse)


        playerurls =  response.xpath("//table[@class = 'sbn-data-table']//td[@class='sbn-data-table-name']/a/@href")
        if len(playerurls) > 0:
            for playerurl in playerurls:
                yield scrapy.Request(playerurl.extract(), callback=self.parse)

        player = response.xpath("//div[@class='sbn-pte-head-player-card']")
        if len(player) > 0:
            item = SBNationPlayer()
            item['Name'] = player.xpath("//h1/text()")[0].extract()
            item['Team'] = player.xpath("//h3/a/text()")[0].extract()
            info = player.xpath("//h3/span/text()")[0].extract().split("\n")[3].replace(" ", "")
            lis = player.xpath("//ul[@class='sbn-pte-head-player-list']/li")
            for li in lis:
                attrName = li.xpath("span/text()")[0].extract().replace(":", "")
                attrValue = li.xpath("text()")[0].extract().replace(" ", "")
                item[attrName] = attrValue
            yield item

