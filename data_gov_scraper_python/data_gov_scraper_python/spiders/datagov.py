# -*- coding: utf-8 -*-
import scrapy
import json
# import csv
import unicodecsv as csv
import re

class DatagovSpider(scrapy.Spider):
    name = 'datagov'
    # allowed_domains = ['https://data.gov.uk/']
    start_urls = [
        'https://data.gov.uk/search?filters%5Btopic%5D=Business+and+economy',
        'https://data.gov.uk/search?filters%5Btopic%5D=Crime+and+justice',
        'https://data.gov.uk/search?filters%5Btopic%5D=Defence',
        'https://data.gov.uk/search?filters%5Btopic%5D=Education',
        'https://data.gov.uk/search?filters%5Btopic%5D=Environment',
        'https://data.gov.uk/search?filters%5Btopic%5D=Government',
        'https://data.gov.uk/search?filters%5Btopic%5D=Government+spending',
        'https://data.gov.uk/search?filters%5Btopic%5D=Health',
        'https://data.gov.uk/search?filters%5Btopic%5D=Mapping',
        'https://data.gov.uk/search?filters%5Btopic%5D=Society',
        'https://data.gov.uk/search?filters%5Btopic%5D=Towns+and+cities',
        'https://data.gov.uk/search?filters%5Btopic%5D=Transport', 
    ]

    saveFile = open("data.csv", "w")
    fieldnames = ['topic', 'title', 'published_by', 'last_updated']
    writer = csv.DictWriter(saveFile, fieldnames=fieldnames, encoding='utf-8')

    writer.writeheader()

    def parse(self, response):

        prefix = 'https://data.gov.uk/search?filters%5Btopic%5D='
        topic = str(response.url).replace(prefix,'').replace('+', ' ').replace('&page=', '')
        topic = re.sub(r'\d+', '', topic)
        
        for article in response.css('div.dgu-results__result'):
            data = {
                'topic': topic,
                'title': article.css('a::text').extract_first(),
                'published_by': article.css('.published_by::text').extract_first(),
                'last_updated': article.css('.last_updated::text').extract_first(),
            }
            
            # self.saveFile.write(str(data))
            self.writer.writerow(data)
            
            yield data

        next_page = response.css('a[rel="next"]::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        # json.dump(data_arr, self.saveFile)
        # self.saveFile.close()

        # 'https://data.gov.uk/search?filters%5Btopic%5D=Business+and+economy',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Crime+and+justice',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Defence',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Education',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Environment',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Government',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Government+spending',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Health',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Mapping',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Society',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Towns+and+cities',
        # 'https://data.gov.uk/search?filters%5Btopic%5D=Transport',