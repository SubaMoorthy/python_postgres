import scrapy
import string
from webcrawler.items import WhoscoredTeamForm3
from webcrawler.items import WhoscoredTeamForm6
from webcrawler.items import WhoscoredTeamStreaks
from webcrawler.items import WhoscoredTeamPerformances


class WhoscoredSpider(scrapy.Spider):
    name = "whoscored"
    allowed_domains = ["whoscored.com"]
    start_urls = ['http://www.whoscored.com/Statistics/Teams']

    def parse(self, response):
        forms6 = response.xpath("substring-before(substring-after(//script[contains(.,'forms6')]/text(), 'forms6 = '),';')").extract()[0]
        forms6 = string.replace(forms6, "\r\n", "")
        forms6 = string.replace(forms6, "\n", "")
        items6 = forms6.split('],')
        keys = ['ID', 'Tournament', '', '', '', '', 'Team', 'OverallP', 'OverallW', 'OverallD', 'OverallL', 'OverallGF', 'OverallGA', 'OverallGD', 'OverallPts',
        'HomeP', 'HomeW', 'HomeD', 'HomeL', 'HomeGF', 'HomeGA', 'HomeGD', 'HomePts',
        'AwayP', 'AwayW', 'AwayD', 'HomeL', 'AwayGF', 'AwayGA', 'AwayGD', 'AwayPts']
        for item6 in items6:
            item6 = string.replace(item6, "[", "")
            item6 = string.replace(item6, "'", "")
            values = item6.split(',')
            item = WhoscoredTeamForm6()
            for i in range(0, 31):
                if i != 2 and i != 3 and i != 4 and i != 5:
                    item[keys[i]] = values[i]
            yield item

        forms3 = response.xpath("substring-before(substring-after(//script[contains(.,'forms3')]/text(), 'forms3 = '),';')").extract()[0]
        forms3 = string.replace(forms3, "\r\n", "")
        forms3 = string.replace(forms3, "\n", "")
        items3 = forms3.split('],')
        keys = ['ID', 'Tournament', '', '', '', '', 'Team', 'OverallP', 'OverallW', 'OverallD', 'OverallL', 'OverallGF', 'OverallGA', 'OverallGD', 'OverallPts',
        'HomeP', 'HomeW', 'HomeD', 'HomeL', 'HomeGF', 'HomeGA', 'HomeGD', 'HomePts',
        'AwayP', 'AwayW', 'AwayD', 'HomeL', 'AwayGF', 'AwayGA', 'AwayGD', 'AwayPts']
        for item3 in items3:
            item3 = string.replace(item3, "[", "")
            item3 = string.replace(item3, "'", "")
            values = item3.split(',')
            item = WhoscoredTeamForm3()
            for i in range(0, 31):
                if i != 2 and i != 3 and i != 4 and i != 5:
                    item[keys[i]] = values[i]
            yield item

        streaks = response.xpath("substring-before(substring-after(//script[contains(.,'streaks')]/text(), 'streaks = '),';')").extract()[0]
        streaks = string.replace(streaks, "\r\n", "")
        streaks = string.replace(streaks, "\n", "")
        streakitems = streaks.split('],')
        keys = ['', 'Team', 'ID', 'Tournament', '', '', '', '', 'OverallStreaks', 'HomeStreaks', 'AwayStreaks', '',
                'OverallPlayed', 'HomePlayed', 'AwayPlayed']
        for sitem in streakitems:
            sitem = string.replace(sitem, "[", "")
            sitem = string.replace(sitem, "'", "")
            values = sitem.split(',')
            item = WhoscoredTeamStreaks()
            for i in range(0, 15):
                if i != 0 and i != 4 and i != 5 and i != 6 and i != 7 and i != 11:
                    item[keys[i]] = values[i]
            yield item

        performances = response.xpath("substring-before(substring-after(//script[contains(.,'performances')]/text(), 'performances = '),';')").extract()[0]
        performances = string.replace(performances, "\r\n", "")
        performances = string.replace(performances, "\n", "")
        pitems = performances.split('],')
        keys = ['', 'Team', 'ID', 'Tournament', '', '', '', '', 'OverallP', 'OverallW', 'OverallD', 'OverallL',
                'OverallGF', 'OverallGA', 'OverallGD', 'OverallPts', 'HomeP', 'HomeW', 'HomeD', 'HomeL', 'HomeGF',
                'HomeGA', 'HomeGD', 'HomePts', 'AwayP', 'AwayW', 'AwayD', 'HomeL', 'AwayGF', 'AwayGA', 'AwayGD',
                'AwayPts']
        for pitem in pitems:
            pitem = string.replace(pitem, "[", "")
            pitem = string.replace(pitem, "'", "")
            values = pitem.split(',')
            item = WhoscoredTeamPerformances()
            for i in range(0, 32):
                if i != 0 and i != 4 and i != 5 and i != 6 and i != 7:
                    item[keys[i]] = values[i]
            yield item