import scrapy
from scrapy import signals
from scrapy import Spider
import datetime
import csv
import unicodedata


class BikeSpider(Spider):
    name = 'tdfspider'
    mydict = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BikeSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider    

    def __init__(self):
        with open('riders.csv', mode='r') as infile:
            reader = csv.reader(infile)
            self.mydict = {rows[0]:[rows[1]] for rows in reader}

    start_urls = []
    for i in range(1,10):
        start_urls = start_urls+[("http://www.letour.fr/le-tour/2017/fr/%d00/classement/bloc-classement-page/ITG.html" % i)]

    def parse(self, response):
        def strip_accents(s):
            return ''.join(c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn')

        for resultat in response.css('tbody').xpath('tr'):
            rank = resultat.xpath('td/text()')[0].extract()
            rider = strip_accents(resultat.xpath('td/a/text()')[0].extract())
            #team = resultat.xpath('td/a/text()')[1].extract()
            rez = self.mydict[rider]
            rez.append(int(rank))
            self.mydict[rider] = rez
      

    def spider_closed(self, spider):
        with open('tdfres.csv', 'wb') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.mydict.items():
                writer.writerow([key.encode('utf-8')]+value)
