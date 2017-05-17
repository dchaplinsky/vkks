# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import Join


class JudgeItem(scrapy.Item):
    name = scrapy.Field()
    section = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


class PdfsSpider(scrapy.Spider):
    name = "pdfs"
    allowed_domains = ["vkksu.gov.ua"]
    start_urls = ['http://vkksu.gov.ua/ua/dieklaracii-rodinnich-zwiazkiw-suddi-ta-dobrotchiesnosti-suddi/dieklaracii-suddiw/',
                  'http://vkksu.gov.ua/ua/dieklaracii-rodinnich-zwiazkiw-suddi-ta-dobrotchiesnosti-suddi/dieklaracii-podani-w-2017-roci/']


    def parse_subpage(self, response):
        for tr in response.css("table.forma tbody tr"):
            section = response.meta["section"]

            num = " ".join(tr.css(":nth-child(1) ::text").extract()).strip()
            name = " ".join(tr.css(":nth-child(2) ::text").extract()).strip()

            if not num[0].isdigit():
                section = name
                name = num

            pdf1 = response.urljoin(
                tr.css(":nth-child(3) a::attr(href)").extract_first())
            pdf2 = response.urljoin(
                tr.css(":nth-child(4) a::attr(href)").extract_first())

            yield JudgeItem(
                name=name,
                section=section,
                file_urls=[pdf1, pdf2]
            )

    def parse(self, response):
        for r in response.css("a.announcement"):

            yield scrapy.Request(
                response.urljoin(r.css("::attr(href)").extract_first()),
                meta={
                    "section": r.css("::text").extract_first()
                },
                callback=self.parse_subpage
            )
