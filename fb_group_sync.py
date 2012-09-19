import urllib2
import urllib
import re
import ConfigParser
import json
import MySQLdb

config = ConfigParser.ConfigParser()
config.read('properties.cfg')
db = MySQLdb.connect(user=config.get('db','user'), passwd=config.get('db','password'), db=config.get('db','name'))
cursor = db.cursor()

def index():
    group_url = config.get('group','url')
    data = urllib2.urlopen(group_url).read()
    jsondata = json.loads(data)
    for i,post in enumerate(jsondata['data']):
        print post.get('id') 
        if(post.get('message') != None):
            comments_count = None
            like_count = None
            if(post.get('comments') != None):
                comments_count = post.get('comments').get('count')
            if(post.get('likes') != None):
                likes_count = post.get('likes').get('count')
        #Do the DB part here
            cursor.execute("""SELECT InsertPost(%s, %s, %s, %s, %s, %s) """,(post.get('from').get('name'), post.get('from').get('id'),post.get('message'),likes_count, comments_count,post.get('id')))
            code = cursor.fetchone()
        # Post urls to Kippt
       	    if(code[0] == 1 and post.get('link') !=  None):
                print post.get('link')
                print post.get('name')
                print post.get('description')
                link = post.get('link').encode("ascii","ignore")
                title = post.get('name').encode("ascii","ignore").replace('"','')
                if(post.get('description') != None):
                    description = post.get('description').encode("ascii","ignore").replace('"','') + '-' + post.get('from').get('name').encode("ascii","ignore")
                else:
                    description = post.get('message').replace('"','') + '-' + post.get('from').get('name').encode('ascii','ignore')
      	        values = '{"url": "'+link+'" , "list":"'+config.get('kippt','listuri')+'", "title":"'+title+'", "notes":"'+description+ '"}'
                print values
                req = urllib2.Request(config.get('kippt','url'),values)
                req.add_header('X-Kippt-Username', config.get('kippt','username'))
                req.add_header('X-Kippt-API-Token', config.get('kippt','apitoken'))
	    
                r = urllib2.urlopen(req)
	        print r.read()
            elif(code[0]==1):
               print post.get('message')
                #make this regex better if you want
	       try:
                   urls =  re.findall("(?P<url>https?://[^\s]+)", post.get('message'))
                   description = post.get('message').replace('"','')
                   for url in urls:
                       description = description.replace("\n"," ")	       
                       description = description.replace(url,"")	       
                   description = description  + '-' + post.get('from').get('name').encode("ascii","ignore").replace('"','')

                   for url in urls:
                       values = '{"url": "'+url+'" , "list": "'+config.get('kippt','listuri')+'", "notes":"'+description+'"}' 
                       req = urllib2.Request(config.get('kippt','url'),values)
                       req.add_header('X-Kippt-Username', config.get('kippt','username'))
                       req.add_header('X-Kippt-API-Token', config.get('kippt','apitoken'))
                       r = urllib2.urlopen(req)
               except:
                   pass


  
if __name__ == "__main__":
    index()
