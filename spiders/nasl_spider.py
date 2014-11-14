import scrapy
import json
from webcrawler.items import NASLPlayer
from webcrawler.items import NASLTeam

class NaslSpider(scrapy.Spider):
    name = "nasl"
    allowed_domains = ["nasl.com"]
    start_urls = ["http://www.nasl.com/stats/players/table", "http://www.nasl.com/stats/teams"]

    def parse(self, response):
        attrlist = []
        teamAttrList = []
        table = response.xpath("//table[@id='playerStatsTable']")
        teamTable = response.xpath("//table[@id='teamStatsTable']")
        if len(table) > 0:
            for attr in table.xpath("thead/tr/th/text()"):
                attrlist.append(attr.extract())
            for tr in table.xpath("tbody/tr"):
                i = 0
                item = NASLPlayer()
                for td in tr.xpath("td/text()"):
                    item[attrlist[i]] = td.extract()
                    i = i + 1
                #scraped_data_player.append(item)
                yield  item


        if len(teamTable) > 0:
            for attr in teamTable.xpath("thead/tr/th/text()"):
                teamAttrList.append(attr.extract())
            for tr in teamTable.xpath("tbody/tr"):
                i = 0
                teamItem = NASLTeam()
                for td in tr.xpath("td/text()"):
                    teamItem[teamAttrList[i]] = td.extract()
                    i = i + 1
                #scrapped_data_team.append(item)
                yield  teamItem


