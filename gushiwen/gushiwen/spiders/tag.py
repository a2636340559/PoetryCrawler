# -*- coding: utf-8 -*-
import scrapy


class TagSpider(scrapy.Spider):
    name = 'tag'
    #allowed_domains = ['https://www.gushiwen.org/shiwen']
    start_urls = ['http://https://www.gushiwen.org/shiwen/']

    def parse(self, response):
        Type=response.css(".sright")[3]
        author={}
        for a in Type.css("a").extract():
            Type1=re.findall(r">.*</a>",a)[0][1:-4]
            print("EEEEEE",re.findall(r">.*</a>",a)[0][1:-4])
            print("DDDDDD",str(re.findall(r".+\.aspx",a)[0].split('/')[2]))
            try:
                href="https://www.gushiwen.org/shiwen/"+re.findall(r".+\.aspx",a)[0].split('/')[2]
            except:
                href="https://www.gushiwen.org/shiwen"
            author.update({"style":Type1,"href":href})
            yield author

