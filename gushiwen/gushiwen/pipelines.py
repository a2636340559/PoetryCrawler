# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import MySQLdb
class GushiwenPipeline(object):
	content=[]
	def open_spider(self,spider):
		self.f=open("style.json",'w')
	def close_spider(self,spider):
		json.dump(self.content,fp=self.f,indent=4)
		self.f.close()
	def process_item(self,item,spider):
		"""
		con=MySQLdb.connect(host='39.106.193.194',user='park',passwd='park',db='poetdb',port=3306,charset='utf8')
		cur=con.cursor()
		cur.execute('insert into Tag values(%s,%s)',("形式",item['style']))
		con.commit()
		con.close()
		print("style",item['style'])
		self.content.append(item)
		"""
		return item
class AuthorPipline(object):
	content=[]
	def open_spider(self,spider):
		self.f=open("author.json",'w')
	def close_spider(self,spider):
		json.dump(self.content,fp=self.f,indent=4)
		self.f.close()
	def process_item(self,item,spider):
		#con=MySQLdb.connect(host='39.106.193.194',user='park',passwd='park',db='poetdb',port=3306,charset='utf8')
		#cur=con.cursor()
		#cur.execute('insert into author values(%s,%s,%s)',(item['name'],item['img'],item['detail']))
		#con.commit()
		#con.close()
		#self.content.append(item)
		return item
class PoetPipline(object):
	content=[]
	def open_spider(self,spider):
		self.f=open("poet.json",'w')
	def close_spider(self,spider):
		json.dump(self.content,fp=self.f,indent=4)
		self.f.close()
	def process_item(self,item,spider):
		con=MySQLdb.connect(host='39.106.193.194',user='park',passwd='park',db='poetdb',port=3306,charset='utf8')
		cur=con.cursor()
		cur.execute('insert into poet values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(item['name'],item['dynasty'],item['author'],item['content'],item['tag'],item['fanyi'],item['zhushi'],item['cankao'],item['shangxi']))
		con.commit()
		con.close()
		self.content.append(item)
		print("nNNNNNNNNN",item["n"])
		return item



