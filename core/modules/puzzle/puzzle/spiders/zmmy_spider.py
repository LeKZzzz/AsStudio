import scrapy
from ..items import ZmmyItem
import re


class ZmmySpider(scrapy.Spider):
    name = 'zmmy_spider'  # 爬虫识别名称
    allowed_domains = ['www.cmiyu.com']  # 域名范围
    start_urls = ['http://www.cmiyu.com/zmmy/']  # 爬取的url元组/列表

    def parse(self, response):  # 翻页
        preurl = 'http://www.cmiyu.com/zmmy/my13{}.html'
        for i in range(1, 372):
            url = preurl.format(i)
            yield scrapy.Request(url=url, callback=self.page_html)

    def page_html(self, response):  # 页面中的跳转url
        preurl = 'http://www.cmiyu.com'
        detail_htmls = response.xpath('/html/body/div[6]/div[1]/div/div[2]/ul')

        for i in range(1, 19):
            next_url = detail_htmls.xpath('li[{}]/a/@href'.format(i)).extract_first()
            url = preurl + next_url
            yield scrapy.Request(url=url, callback=self.item_html)

    def item_html(self, response):  # 谜语html
        item = ZmmyItem()
        if re.match('^\u5c0f\u8d34\u58eb',
                    str(response.xpath('/html/body/div[6]/div[1]/div[1]/div[3]/p/text()').extract_first())):  # 判断是否存在小贴士
            item['mystery'] = response.xpath('/html/body/div[6]/div[1]/div[1]/div[4]/h3[1]/text()').extract_first()
            item['tips'] = response.xpath('/html/body/div[6]/div[1]/div[1]/div[3]/p/text()').extract_first()
            item['answer'] = response.xpath('/html/body/div[6]/div[1]/div[1]/div[4]/h3[2]/text()').extract_first()
        else:
            item['mystery'] = response.xpath('/html/body/div[6]/div[1]/div[1]/div[3]/h3[1]/text()').extract_first()
            item['tips'] = "小贴士：无"
            item['answer'] = response.xpath('/html/body/div[6]/div[1]/div[1]/div[3]/h3[2]/text()').extract_first()
        yield item  # 调用pipeline
