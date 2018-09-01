# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    def parse(self, response):
        content_lefts=response.xpath(".//div[@id='content-left']/div")
        for content_left in content_lefts:
            author=content_left.xpath(".//h2/text()").get().strip()
            #get转码

            content="".join(content_left.xpath(".//div[@class='content']//text()").getall()).strip()
            # duanzi ={"author":author,"content":content}
            item =QsbkItem(author=author,content=content)
            yield item
        next_url =response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            nexturl="https://www.qiushibaike.com"+next_url
            yield scrapy.Request(nexturl,self.parse)
            #将一个个nexturl传给parse
            #scrapy.request类，像url发送请求并用parse函数


