# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp.items import WxappItem

class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),
        #如果只想获取url不需要callback回调函数
        Rule(LinkExtractor(allow=r'.+article-.+\.html'),callback="parse_detail",follow=False)
    )
    def parse_detail(self, response):
        title=response.xpath("//h1[@class='ph']/text()").get()
        author_p =response.xpath("//p[@class='authors']")
        author =author_p.xpath(".//a/text()").get()
        time =author_p.xpath(".//span/text()").get()
        content =response.xpath("//td[@id='article_content']//text()").getall()
        content ="".join(content).strip()
        item =WxappItem(title=title,author=author,time=time,content=content)
        yield item
        print('author:%s/pub_time:%s'%(author,time))
        print(title)
        print(content)

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
