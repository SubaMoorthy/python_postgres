import scrapy
import re
import string
import urlparse
import json
from webcrawler.items import USLPlayerRos
from webcrawler.items import USLPlayerStat
from webcrawler.items import USLTeam

class linksSpider(scrapy.Spider):
    name = 'usl'
    allowed_domains = ['uslpro.uslsoccer.com']
    start_urls = ['http://uslpro.uslsoccer.com/players/index_E.html', 'http://uslpro.uslsoccer.com/standings/index_E.html']

    def parse(self, response):
        table1 = response.xpath('//table//table//table//table//table//table')
        statslinks = table1.xpath("tbody/tr/td[last()]//a/@href")
        for url in statslinks:
            yield scrapy.Request(url.extract(), callback=self.parse)

        pattern = re.escape("$j('div#indicator').fadeIn();") + '\s*url\s*=\s*(.*);'
        match = response.selector.re(pattern)
        if len(match) >= 1:
            rosUrl = response.selector.re(pattern)[0]
            rosUrlStr = urlparse.urljoin(response.url, string.replace(rosUrl, "'", ""))
            statUrl = response.selector.re(pattern)[1]
            statUrlStr = urlparse.urljoin(response.url, string.replace(statUrl, "'", ""))
            yield scrapy.Request(rosUrlStr, callback=self.parse)
            yield scrapy.Request(statUrlStr, callback=self.parse)

        table2 = response.xpath('//table//table//table//table//table//table')
        trs = table2.xpath("//tr[@class='tms']")
        attrs = ["OverallPts", "OverallGP", "OverallW", "OverallL", "OverallT", "OverallGF", "OverallGA", "HomeW",
                 "HomeL", "HomeT", "HomeGF", "HomeGA", "AwayW", "AwayL", "AwayT", "AwayGF", "AwayGA"]
        for tr in trs:
            team = USLTeam()
            teamname = tr.xpath("td[@class = 'stub']/a/text()")[0].extract()
            teamname = string.replace(teamname, "\r\n", "")
            teamname = teamname.strip()
            team['TeamName'] = teamname
            i = 0
            for td in tr.xpath("td[not (@class)]/text()"):
                team[attrs[i]] = td.extract()
                i = i +1
            yield team

        if response.url.endswith('ros.js'):
            rosstr = response.xpath("//body/p/text()")[0].extract().replace("\r\n", "").replace("\n", "")
            rosplayers = json.loads(rosstr)
            for id, player in rosplayers["players"].items():
                rositem = USLPlayerRos()
                for key, value in player.items():
                    rositem[key] = value
                yield rositem

        if response.url.endswith('stat.js'):
            statstr = response.xpath("//body/p/text()")[0].extract().replace("\r\n", "").replace("\n", "")
            statplayers = json.loads(statstr)
            for id, player in statplayers["players"].items():
                statitem = USLPlayerStat()
                for key, value in player.items():
                    statitem[key] = value
                yield statitem