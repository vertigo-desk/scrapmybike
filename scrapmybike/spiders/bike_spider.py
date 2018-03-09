import scrapy
from scrapy import signals
from scrapy import Spider
import datetime
import logging
import csv
from rez import Rez
from race import Race

class BikeSpider(Spider):
    name = 'bikespider'
    riders = set()
    start_urls = ['http://www.procyclingstats.com/races.php?year=2018&circuit=13&ApplyFilter=Filter']

    #start_urls = ['http://www.procyclingstats.com/race/Trofeo_Porreres,_Felanitx,_Ses_Salines,_Campos_2017']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BikeSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider 

    def parse(self, response):
        # follow links to races pages
        #for href in response.css('a::attr(href)').re(r'race\.php.*=2'):
         #   yield response.follow(href, self.parse)


        # follow pagination links
        for href in response.selector.xpath("//table/tr/td/a[re:test(@href, '2018$')]/@href").extract():
            yield response.follow(href, self.parse_race)

 

    def parse_race(self, response):
        
        # race title
        race_name = response.xpath('//h1/text()').extract()[0]
        race_name = race_name[13:]
        race = Race(race_name)
        
        # result tab
        for tr in response.xpath('//div[re:test(@class, "show")]/table[contains(@class, "basic")]/tbody/tr'):
            rank = tr.xpath('td/text()').extract_first()
            rider = tr.xpath('td/a/@href')[0].re_first(r'rider\/(.*)')
            team = tr.xpath('td/a/@href')[1].re_first(r'team\/(.*)')
            self.riders.add((str(rider),str(team)))
            rez = Rez(rank,rider)
            race.listResults.append(rez)

    def spider_closed(self, spider):
        # logging.warning(self.riders)
        logging.warning(filter(lambda x: x[1].startswith('fortuneo-samsic-2018'), self.riders))

        
        with open('list_riders.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            #writer.writerow(self.riders)

'''

        ranks = response.xpath('//span[contains(@class, "show")]/span[not(contains(@class, "time")) and not(contains(@style,"tahoma"))]/text()').re(r'(\d+)')
        maxrank = max(map(int, ranks))

        datestr = str(response.selector.xpath('//div[@class="subDiv info show"]/text()[1]').extract_first())
        datestr = datestr+ " " + str(response.selector.xpath('//div[@class="subDiv info show"]/text()[2]').extract_first())
        date = datetime.datetime.strptime(datestr, ' %d %B %Y')
        datestr = date.strftime('%d-%m-%Y')

        race = response.xpath('//h1/text()').extract()

        yield {
                    'race' : race,
                    'date' : datestr,
                    'rank': maxrank,
                    'rider' : 'nbcoureurs',
                    'team' : 'all',
        }    
        for resultat in response.xpath('//div[contains(@class, "line str")]'):
            rank = resultat.xpath('span[contains(@class, "show")]/span[not(contains(@class, "time"))]/text()').extract_first()
            rider = resultat.xpath('span/a[@class="rider "]/@href').re_first(r'rider\/(.*)')
            team = resultat.xpath('span/a[@class="rider "]/@href').re_first(r'team\/(.*)')
            if ((rank.isdigit()) and (not(rider is None)) and (not(team is None))):
                yield {
                    'race' : race,
                    'date' : datestr,
                    'rank': rank,
                    'rider' : rider,
                    'team' : team,
                }
            
         '''   
