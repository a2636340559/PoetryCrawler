# -*- coding: utf-8 -*-
import scrapy
import re


class AuthorSpider(scrapy.Spider):
    name = 'author'
    #allowed_domains = ['https://so.gushiwen.org/authors']
    start_urls = ['https://so.gushiwen.org/authors/default.aspx?p=776&c=%E4%B8%8D%E9%99%90']

    def parse(self, response):
    	nextpage=response.css("form .pagesright .amore").css("a::attr(href)").extract()
    	authorDict={}
    	names=response.css(".sonspic .cont p b").extract()
    	imgs=response.css(".sonspic .cont a img[src^='https']").css("img::attr(src)").extract()
    	details=response.css(".sonspic .cont p").extract()
    	#print("NNNNNNNN",len(names))
    	#print("IIIIIIIIIIII",len(imgs))
    	#print("DDDDDDDD",len(details))
    	for index in range(len(names)):
    		name=re.findall(r">.+<",names[index])[0][1:-1]
    		detail=re.findall(r">.+<a",details[2*index+1])[0][1:-2]
    		if(index>=len(imgs)):
    			authorDict.update({"name":name,"img":'',"detail":detail})
    		else:
    			authorDict.update({"name":name,"img":imgs[index],"detail":detail})
    		yield authorDict
    	if nextpage:
    		url="https://so.gushiwen.org"+nextpage[0]
    		#print("URLLLLLLLLLLL",url)
    		yield scrapy.Request(url,callback=self.parse)
    


