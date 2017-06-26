import scrapy



class BikeSpider(scrapy.Spider):
    name = 'bikespider'

    start_urls = ['http://www.procyclingstats.com/races.php?year=2017&circuit=13&ApplyFilter=Filter']

    #start_urls = ['http://www.procyclingstats.com/race/Trofeo_Porreres,_Felanitx,_Ses_Salines,_Campos_2017']

    def parse(self, response):
        # follow links to races pages
        for href in response.css('a::attr(href)').re(r'race\.php.*=2'):
            yield response.follow(href, self.parse)


        # follow pagination links
        for href in response.selector.xpath("//a[contains(text(),'Result')]/@href").extract():
            yield response.follow(href, self.parse_race)

 

    def parse_race(self, response):
        for resultat in response.xpath('//div[contains(@class, "line str")]'):
            day = str(response.selector.xpath('//div[@class="subDiv info show"]/text()[1]').extract_first())
            day = day+ " " + str(response.selector.xpath('//div[@class="subDiv info show"]/text()[2]').extract_first())
            ranks = response.xpath('//span[contains(@class, "show")]/span[not(contains(@class, "time")) and not(contains(@style,"tahoma"))]/text()').re(r'(\d+)')
            maxrank = max(map(int, ranks))
            
            yield {
                'race' : response.xpath('//h1/text()').extract(),
                'date' : day,
                'finishers' : maxrank,
                'rank': resultat.xpath('span[contains(@class, "show")]/span[not(contains(@class, "time"))]/text()').extract_first(),
                'rider' : resultat.xpath('span/a[@class="rider "]/@href').re_first(r'rider\/(.*)'),
                'team' : resultat.xpath('span/a[@class="rider "]/@href').re_first(r'team\/(.*)'),
            }
