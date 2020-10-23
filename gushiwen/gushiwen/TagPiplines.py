"""
class TagPipeline(object):
    content=[]
    def open_spider(self,spider):
    	self.f=open("style.json",'w')
    def close_spider(self,spider):
    	json.dump(self.content,fp=self.f,indent=4)
    	self.f.close()
    def process_otem(self,item,spider):
		con=MySQLdb.connect(host='xx.xx.xx.xx',user='xx',passwd='xx',db='xx',port=xx,charset='utf8')
		cur=con.cursor()
		cur.execute('insert into Tag values(%s,%s)',("形式",item['style']))
		con.commit()
		con.close()
		print("style",item['style'])
		self.content.append(item)
		return item
	""" 
   
