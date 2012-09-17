import urllib2
import urllib
import re
import ConfigParser
import json

config = ConfigParser.ConfigParser()
config.read('properties.cfg')

def index():
    group_url = config.get('group','url')
    data = urllib2.urlopen(group_url).read()
    jsondata = json.loads(data)
    for i,post in enumerate(jsondata['data']):
        print post.get('id') 
        #Do the DB part here

        # Post urls to Kippt
       	if(post.get('link') !=  None):
            print post.get('link')
            print post.get('name')
            print post.get('description')
            link = post.get('link').encode("ascii","ignore")
            name = post.get('name').encode("ascii","ignore")
            description = post.get('description').encode("ascii","ignore") + '\n' + post.get('from').get('name').encode("ascii","ignore")
	    values = '{"url": "'+link+'" , "list":"'+config.get('kippt','listuri')+'", "title":"'+name+'", "notes":"'+description+ '"}'
            print values
            req = urllib2.Request(config.get('kippt','url'),values)
            req.add_header('X-Kippt-Username', config.get('kippt','username'))
            req.add_header('X-Kippt-API-Token', config.get('kippt','apitoken'))
	    
            r = urllib2.urlopen(req)
	    print r.read()
        elif(post.get('message') !=  None):
           print post.get('message')
            #make this regex better if you want
	   try:
               urls =  re.findall("(?P<url>https?://[^\s]+)", post.get('message'))
               description = post.get('message')
               for url in urls:
                   description.replace(url,"")	       
               description = description  + '\n' + post.get('from').get('name').encode("ascii","ignore")

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
