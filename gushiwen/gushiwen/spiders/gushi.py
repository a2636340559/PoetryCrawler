# -*- coding: utf-8 -*-
import scrapy
import re
from w3lib.html import remove_tags

class GushiSpider(scrapy.Spider):
    name = 'gushi'
    #allowed_domains = ['https://www.gushiwen.org/shiwen/']
    start_urls = ['https://www.gushiwen.org/shiwen/']
    n=0
    

    def parse(self, response):
        nextpage=response.css("form .pagesright .amore").css("a::attr(href)").extract()
        url=response.css(".cont p a[target=_blank]").css("a::attr(href)").extract()
        for item in url:
            yield scrapy.Request(item,callback=self.poet_parse)
        print("DDDDDDDDDDDDD",nextpage[0])
        if nextpage:
            yield response.follow(nextpage[0],callback=self.parse)
    def poet_parse(self,response):
        itemDict={}
        title=re.findall(r">.+</h1>",response.css(".cont h1").extract()[0])[0][1:-5]
        author=re.findall(r">.+</a>",response.css(".cont .source a[href^='/']").extract()[0])[0][1:-4]
        dynasty=re.findall(r">.+</a>",response.css(".cont .source a[href^='https']").extract()[0])[0][1:-4]
        content=''
        Tag="暂无标签"
        if(response.css(".cont .contson")[0].css("p").extract()):
            for line in response.css(".cont .contson")[0].css("p").extract():
                content+=re.findall(r">.+<",line)[0][1:-1]
        else:
            content=re.findall(r".+",response.css(".cont .contson")[0].extract())[1]
        if(response.css(".sons .tag").extract()):
            Tag=""
            for tag in response.css(".sons .tag")[0].css("a").extract():
                Tag+=re.findall(r">.+<",tag)[0][1:-1]+" "
        #print("Tag:",Tag)
        Id=""
        Id1=""
        itemDict.update({"name":title,"dynasty":dynasty,"author":author,"content":remove_tags(content),"tag":Tag})
        if (response.css(".left div[id^='fanyi']").extract()):
            Id=re.findall(r"fanyi\d+",response.css(".left div[id^='fanyi']").extract()[0])[0][5:]
        if(response.css(".left div[id^='shangxi']").extract()):
            Id1=re.findall(r"shangxi\d+",response.css(".left div[id^='shangxi']").extract()[0])[0][7:]
        if(Id and Id1):
            request=scrapy.Request("https://so.gushiwen.org/shiwen2017/ajaxfanyi.aspx?id="+Id,callback=self.yizhu)
            request.meta['id']=Id1
            request.meta['itemDict']=itemDict
            yield request
        elif(Id):
            request=scrapy.Request("https://so.gushiwen.org/shiwen2017/ajaxfanyi.aspx?id="+Id,callback=self.yizhu)
            request.meta['itemDict']=itemDict
            request.meta['id']=Id1
            yield request
        elif(Id1):
            content=""
            fanyi="暂无翻译"
            zhushi="暂无注释"
            if(response.css(".sons .contyishang").extract()):
                fanyi=""
                zhushi=""
                for item in response.css(".sons .contyishang")[0].css("p").extract():
                    content+=item
                content=remove_tags(content.replace("<br>","/n"))[4:]
                fanyi=content.split("注释")[0]
                zhushi=content.split("注释")[1]
            cankao="暂无参考"
            temp=response.css(".cankao div span").extract()
            if(temp):
                cankao=""
                for index in range(len(temp)):
                    cankao+=remove_tags(temp[index])
                    if(index%2==1):
                        cankao+="/n"
            itemDict.update({"fanyi":fanyi,"zhushi":zhushi,"cankao":cankao})
            request=scrapy.Request("https://so.gushiwen.org/shiwen2017/ajaxshangxi.aspx?id="+Id1,callback=self.shangxi)
            request.meta['itemDict']=itemDict
            yield request
        else:
            content=""
            fanyi="暂无翻译"
            zhushi="暂无注释"
            if(response.css(".sons .contyishang").extract()):
                fanyi=""
                zhushi=""
                for item in response.css(".sons .contyishang")[0].css("p").extract():
                    content+=item
                content=remove_tags(content.replace("<br>","/n"))[4:]
                fanyi=content.split("注释")[0]
                zhushi=content.split("注释")[1]
            cankao="暂无参考"
            temp=response.css(".cankao div span").extract()
            if(temp):
                cankao=""
                for index in range(len(temp)):
                    cankao+=remove_tags(temp[index])
                    if(index%2==1):
                        cankao+="/n"
            self.n+=1
            itemDict.update({"fanyi":fanyi,"zhushi":zhushi,"cankao":cankao,"shangxi":"暂无赏析","n":self.n})
            yield itemDict
    def yizhu(self,response):
        Id=response.meta['id']
        itemDict=response.meta['itemDict']
        content=""
        fanyi="暂无翻译"
        zhushi="暂无注释"
        if(response.css(".sons .contyishang").extract()):
            fanyi=""
            zhushi=""
            for item in response.css(".contyishang p").extract():
                content+=item
            content=remove_tags(content.replace("<br>","/n"))[4:]
        if(content):
            fanyi=content.split("注释")[0]
            zhushi=content.split("注释")[1]
        #fanyi=remove_tags(response.css(".contyishang p").extract()[0].replace("<br>","/n"))[4:]
        #zhushi=remove_tags(response.css(".contyishang p").extract()[1].replace("<br>","/n"))[4:]
        temp=response.css(".cankao div span").extract()
        cankao="暂无参考"
        if(temp):
            cankao=""
            for index in range(len(temp)):
                cankao+=remove_tags(temp[index])
                if(index%2==1):
                    cankao+="/n"
        itemDict.update({"fanyi":fanyi,"zhushi":zhushi,"cankao":cankao})
        if (Id):
            request=scrapy.Request("https://so.gushiwen.org/shiwen2017/ajaxshangxi.aspx?id="+Id,callback=self.shangxi)
            request.meta['itemDict']=itemDict
            yield request
        else:
            self.n+=1
            itemDict.update({"shangxi":"暂无赏析","n":self.n})
            yield itemDict
        #print("FANYI",fanyi)
    def shangxi(self,response):
        itemDict=response.meta['itemDict']
        temp=response.css(".contyishang p").extract()
        shangxi="暂无赏析"
        if(temp):
            shangxi=""
            for item in temp:
                shangxi+=remove_tags(item.replace("</p>","/n"))
        self.n+=1
        itemDict.update({"shangxi":shangxi,"n":self.n})
       # print("PoetPPPPPP",str(itemDict))

        yield itemDict


        




        
            
            
