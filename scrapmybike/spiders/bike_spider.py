import scrapy



class BikeSpider(scrapy.Spider):
    name = 'bikespider'

    start_urls = ['http://www.procyclingstats.com/races.php?year=2017&circuit=13&ApplyFilter=Filter']

    def parse(self, response):
        # follow links to races pages
        for href in response.css('a::attr(href)').re(r'race\.php.*=2'):
            yield response.follow(href, self.parse)

        # follow pagination links
        for href in response.selector.xpath("//a[contains(text(),'Result')]/@href").extract():
            yield response.follow(href, self.parse_race)

    def parse_race(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }
