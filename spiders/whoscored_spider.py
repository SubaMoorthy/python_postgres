import scrapy
import json

class WhoscoredSpider(scrapy.Spider):
    name = "whoscored"
    allowed_domains = ["whoscored.com"]
    start_urls = ["http://www.whoscored.com/StatisticsFeed/1/GetPlayerStatistics?category=summary&subcategory=all&statsAccumulationType=0&isCurrent=true&playerId=&teamIds=&matchId=&stageId=&tournamentOptions=2,3,4,5,22&sortBy=Rating&sortAscending=&age=&ageComparisonType=&appearances=&appearancesComparisonType=&field=Overall&nationality=&positionOptions=&timeOfTheGameEnd=&timeOfTheGameStart=&isMinApp=true&page=&includeZeroValues=&numberOfPlayersToPick=1500"]

    def parse(self, response):
        players = json.loads(response.body)
        i = 1
        for player in players['playerTableStats']:
            print "Player", i
            for key, value in player.items():
                print key, ":", value
            i = i + 1
