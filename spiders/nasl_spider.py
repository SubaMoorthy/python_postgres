import scrapy
from webcrawler.items import NASLPlayer1
from webcrawler.items import NASLPlayer2
from webcrawler.items import NASLTeam
import string

class NaslSpider(scrapy.Spider):
    name = "nasl"
    allowed_domains = ["nasl.com"]
    start_urls = ["http://www.nasl.com/stats/players/table", "http://www.nasl.com/stats/teams", "http://www.nasl.com/players"]

    def parse(self, response):
        attrlist = []
        teamAttrList = []
        table = response.xpath("//table[@id='playerStatsTable']")
        table = response.xpath('//table[@id="playerStatsTable"]')
        teamTable = response.xpath("//table[@id='teamStatsTable']")
        if len(table) > 0:
            for attr in table.xpath("thead/tr/th/text()"):
                attrlist.append(string.replace(attr.extract(), " ", ""))
            if len(attrlist) == 6:
                for tr in table.xpath("tbody/tr"):
                    item = NASLPlayer1()
                    i = 0
                    for td in tr.xpath("td/text()"):
                        item[attrlist[i]] = td.extract()
                        i = i + 1
                    yield item
            elif len(attrlist) == 5:
                trs = table.xpath("//tr")
                for tr in trs:
                    tds = tr.xpath("td[contains(concat(' ',normalize-space(@class), ' '), ' playerStatColor1 ') or "
                                   "contains(concat(' ', normalize-space(@class), ' '), ' playerStatColor2 ')]/text()")
                    if len(tds) > 0:
                        item = NASLPlayer2()
                        i = 0
                        for td in tds:
                            value = td.extract()
                            value = string.replace(value, "\r\n", "")
                            value = string.replace(value, "\n", "")
                            value = value.strip()
                            item[attrlist[i]] = value
                            i = i+1
                        yield item

        if len(teamTable) > 0:
            for attr in teamTable.xpath("thead/tr/th/text()"):
                teamAttrList.append(attr.extract())
            for tr in teamTable.xpath("tbody/tr"):
                i = 0
                teamItem = NASLTeam()
                for td in tr.xpath("td/text()"):
                    teamItem[teamAttrList[i]] = td.extract()
                    i = i + 1
                yield teamItem

        keys = ['PlayerName', 'Team', 'Position', 'DOB', 'Country']