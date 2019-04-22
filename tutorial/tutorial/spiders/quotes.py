# -*- coding: utf-8 -*-
import scrapy
from ..items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'  # 每个项目唯一的名字，来区分不同的Spider
    allowed_domains = ['quotes.toscrape.com']  # 允许爬的域名
    start_urls = ['http://quotes.toscrape.com/']  # 启动时爬取的url列表

     # 定义解析方法
    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item
        next = response.css('.pager .next a::attr("href")').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
