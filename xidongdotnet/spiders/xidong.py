# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
from xidongdotnet.items import XidongdotnetItem
import re


class XidongSpider(scrapy.Spider):
    name = "xidong"
    allowed_domains = ["xidong.net"]
    start_urls = (
        'http://xidong.net/sitemap.html',
    )

    def parse(self, response):
    	for linka in response.xpath('//a/@href').re(r'\/List\d{3}\/\w{12,14}\.html'):
    		url = 'http://xidong.net' + linka
    		yield scrapy.Request(url, callback=self.parse_pageb)

    def parse_pageb(self, response):
    	for linkb in response.xpath('//a/@href').re(r'\/File\d{3}\/\w{9,12}\.html'):
    		url = 'http://xidong.net' + linkb
    		yield scrapy.Request(url, callback=self.parse_pagec)
        try:
            nextpage = response.xpath('//table[@width="590"]//a').re(ur'(?<=\<a href=")\/List\d{3}\/\w{12,14}\.html(?="\>下一页\<\/a\>)')[0]
            if nextpage:
                nextpage = "http://xidong.net" + nextpage
                yield scrapy.Request(nextpage, callback=self.parse_pageb)
        except:
            pass

    def parse_pagec(self, response):
    	item = XidongdotnetItem()
    	a = response.xpath('//div[@id="xdnav-content"]/a[1]/text()').extract()
        b = response.xpath('//div[@id="xdnav-content"]/a[2]/text()').extract()
        c = response.xpath('//div[@id="xdnav-content"]/a[3]/text()').extract()
        d = response.xpath('//div[@id="xdnav-content"]/a[4]/text()').extract()
        if a:
    	    item['Source'] = a
    	if b:
    		item['CategoryA'] = b
    	if c:
    		item['CategoryB'] = c
    	if d:
    		item['CategoryC'] = d
    	item['CategoryName'] = response.xpath('//div[@id="xdintrobg"]/h1/text()').extract()
    	item['FileDiscription'] = response.xpath('//div[@class="content"]/text()').extract()

        filenames = response.xpath('//table[@class="emuletable"]//a/text()').extract()
        try:
            filenames.pop(0)
        except:
            pass
        item['FileNames'] = filenames

        filelinks = response.xpath('//table[@class="emuletable"]//a/@href').extract()
        try:
            filelinks.pop(0)
        except:
            pass
        item['FileLinks'] = filelinks
    	
    	yield item

        
