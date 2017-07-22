import scrapy
from scrapy import signals
from scrapy import Spider
import datetime
import csv
import unicodedata
import re


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
            self.mydict = {rows[0]:[rows[1],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] for rows in reader}

    start_urls = []
    for i in range(1,22):
        start_urls = start_urls+[("http://www.letour.fr/le-tour/2017/fr/%d00/classement/bloc-classement-page/ITG.html" % i)]

    def parse(self, response):
        def strip_accents(s):
            return ''.join(c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn')

        # extract stage number from url
        etape = response.url
        m = re.search('http://www.letour.fr/le-tour/2017/fr/(.+?)00/classement/bloc-classement-page/ITG.html', etape)
        if m:
            no_etape = m.group(1)

        # extract all results from stage
        for resultat in response.css('tbody').xpath('tr'):
            rank = resultat.xpath('td/text()')[0].extract()
            rider = strip_accents(resultat.xpath('td/a/text()')[0].extract())
            #team = resultat.xpath('td/a/text()')[1].extract()
            rez = self.mydict[rider]
            #rez.append(int(rank))
            rez[int(no_etape)] =  int(rank)
            self.mydict[rider] = rez
      

    def spider_closed(self, spider):
        with open('tdfres.csv', 'wb') as csv_file:
            writer = csv.writer(csv_file)
            fortuneo = ["FEILLU Brice", "PICHON Laurent", "BOUET Maxime", "PERICHON Pierre-Luc", "MC LAY DANIEL", "VACHON Florian", "HARDY Romain","GESBERT Elie", "SEPULVEDA Eduardo", "BARDET Romain","BAKELANTS Jan","DOMONT Axel","FRANK Mathias","GASTAUER Ben","GAUTIER Cyril","LATOUR Pierre-Roger","NAESEN Oliver","VUILLERMOZ Alexis"]
            writer.writerow(["epreuve", "nbcoureurs"]+(map(lambda s: s.replace(" ", "_"), fortuneo)))

            
            for i in range(1,22):
                result_etape = []
                for rider in fortuneo:
                    result_etape.append(self.mydict[rider][i])

                writer.writerow([i]+[198]+result_etape)

            '''for key, value in self.mydict.items():
                writer.writerow([key.encode('utf-8')]+value)
            '''
