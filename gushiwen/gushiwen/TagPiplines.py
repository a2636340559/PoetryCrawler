"""
class TagPipeline(object):
    content=[]
    def open_spider(self,spider):
    	self.f=open("style.json",'w')
    def close_spider(self,spider):
    	json.dump(self.content,fp=self.f,indent=4)
    	self.f.close()
    def process_otem(self,item,spider):
		con=MySQLdb.connect(host='39.106.193.194',user='park',passwd='park',db='poetdb',port=3306,charset='utf8')
		cur=con.cursor()
		cur.execute('insert into Tag values(%s,%s)',("形式",item['style']))
		con.commit()
		con.close()
		print("style",item['style'])
		self.content.append(item)
		return item
	""" 
   
