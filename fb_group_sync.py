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
        #if(post.get('message') !=  None):
        #    print post.get('message')
            #make this regex better if you want
	#    try:
                #urls =  re.findall("(?P<url>https?://[^\s]+)", post.get('message'))
		#Post the urls to Kippt
                #for url in urls:
         #           req = urllib2.Request('')
         #           req.add_header('X-Kippt-Username', 'yeskarthik')
         #           req.add_header('X-Kippt-API-Token','1d3bacd51c5d0e9ecd90d527ac013b723513a48c')
         #           req.add_header('data','{"url": '+url+', "list": "/api/lists/157407/"}')
                    
         #           r = urllib2.urlopen(req)
         #   except:
         #       pass

	if(post.get('link') !=  None):
            print post.get('link')
            print post.get('name')
            print post.get('description')
            link = post.get('link').encode("ascii","ignore")
            name = post.get('name').encode("ascii","ignore")
            description = post.get('description').encode("ascii","ignore")
	    #values={"url": post.get('link'), "list": "/api/lists/157407/", "title":post.get('name'),"notes":post.get('description')}
	    values = '{"url": "'+link+'" , "list": "/api/lists/157407/", "title":"'+name+'", "notes":"'+description+'"}'
            print values
#	    data = urllib.urlencode(values)	
#	    data = data.encode('utf-8')
            req = urllib2.Request('https://kippt.com/api/clips/',values)
            req.add_header('X-Kippt-Username', 'yeskarthik')
            req.add_header('X-Kippt-API-Token','1d3bacd51c5d0e9ecd90d527ac013b723513a48c')
	    
            r = urllib2.urlopen(req)
	    print r.read()
    
  
if __name__ == "__main__":
    index()
