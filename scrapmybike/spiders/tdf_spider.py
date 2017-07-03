import scrapy
import datetime


class BikeSpider(scrapy.Spider):
    name = 'tdfspider'

    start_urls = ['http://www.letour.fr/le-tour/2017/fr/300/classement/bloc-classement-page/ITE.html']

    '''def parse(self, response):
        # follow links to races pages
        for href in response.css('a::attr(href)').re(r'race\.php.*=2'):
            yield response.follow(href, self.parse)


        # follow pagination links
        for href in response.selector.xpath("//a[contains(text(),'Result')]/@href").extract():
            yield response.follow(href, self.parse_race)
    '''
 

    def parse(self, response):
        
        for resultat in response.css('tbody').xpath('tr'):
            rank = resultat.xpath('td/text()')[0].extract()
            rider = resultat.xpath('td/a/text()')[0].extract()
            team = resultat.xpath('td/a/text()')[1].extract()
            yield {
                'rank': rank,
                'rider' : rider,
                'team' : team,
            }
            
            
