# \usr\bin\evn python
# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from scrapy.loader import ItemLoader
from hao123.items import  Hao123Item
class HaoSpider(CrawlSpider):
    name = 'dytt'
    start_urls = ['http://www.dygang.net']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

    rules = (Rule(LinkExtractor(allow=('\d+/\d+\.htm'),restrict_xpaths=r'//td/a'),callback='parse_item',follow=True),)

    def parse_item(self,response):
        item = ItemLoader(item=Hao123Item(),response=response)
        item.add_xpath('name',r"//div[@class='title']/a[1]/text()")
        item.add_xpath('time',r"//td[contains(text(),'时间')][1]",re='\d+-\d+-\d')
        item.add_xpath('down',r"//a[@rel='nofollow'][@href]")
        if not 'down' in item.load_item():
            item.add_xpath('down',r"//a[contains(@href,'magnet')]/@href")
        item.add_xpath('description',r"//td[@id='dede_content']")
        return item.load_item()

    def make_requests_from_url(self, url):
        return Request(url,headers=self.headers)