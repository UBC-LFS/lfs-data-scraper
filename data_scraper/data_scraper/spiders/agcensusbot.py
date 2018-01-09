# -*- coding: utf-8 -*-
import scrapy


class AgcensusbotSpider(scrapy.Spider):
    name = 'agcensusbot'
    allowed_domains = ['http://agcensus.dacnet.nic.in/tehsilsummarytype.aspx']
    start_urls = ['http://agcensus.dacnet.nic.in/tehsilsummarytype.aspx/']

    def parse(self, response):
        print('RESULTS FROM SCRAPE:')
        print(response.xpath('//*[@id="_ctl0_ContentPlaceHolder1_ddlState"]').extract())
