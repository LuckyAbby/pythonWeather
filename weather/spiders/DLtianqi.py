# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem

class DltianqiSpider(scrapy.Spider):
    name = 'DLtianqi'
    allowed_domains = ['http://www.tianqi.com']
    start_urls = []

    citys = ['jingzhou', 'hangzhou', 'dalian']

    for city in citys:
        start_urls.append('http://www.tianqi.com/' + city + '/15')

    def parse(self, response):
        items = []
        divLists = response.xpath('//div[@class="table_day "]')
        for div in divLists:
            item = WeatherItem()
            item['date'] = div.xpath('./h3/b/text()').extract()[0]
            item['week'] = div.xpath('./h3/text()').extract()[0]
            item['img'] = div.xpath('./ul/li[@class="img"]/img/@src').extract()[0]
            item['temp'] = div.xpath('./ul/li[@class="temp"]').xpath('string(.)').extract()[0]
            item['air'] = div.xpath('./ul/li[@class="air"]/b/@title').extract()[0]
            item['wind'] = div.xpath('./ul/li[4]/text()').extract()[0]
            items.append(item)
        return items
