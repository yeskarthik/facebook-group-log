import urllib2
import urllib
import re
import ConfigParser
import json
import MySQLdb
import logging
import traceback
from datetime import datetime

class FbGroupArchiver:

    def __init__(self, config_filename):
        self.config = ConfigParser.ConfigParser()
        try:
            self.config.read(config_filename)
        except:
            print 'Config file'+str(config_filename)+' cannot be read'
            return
        config = self.config
        self.db = MySQLdb.connect(user=config.get('db','user'), passwd=config.get('db','password'), db=config.get('db','name'))
        self.cursor = self.db.cursor()
        logging.basicConfig(filename=config.get('logging','infolog'), level=logging.INFO)

    def process_data(self, group_url=None):
        controlchar_regex = re.compile(r'[\n\r\t]')
        cursor = self.cursor
        config = self.config
        if(group_url == None):
            group_url = config.get('group','url')
        data = urllib2.urlopen(group_url).read()
        jsondata = json.loads(data)
        for i,post in enumerate(jsondata['data']):
            try:
                print post.get('id')
                post_id = post.get('id')
                message = post.get('message')
                author_name = post.get('from').get('name').encode('ascii','ignore').replace('"','')
                author_id = post.get('from').get('id')
                
                if(message != None):
                    message = message.encode('ascii','ignore').replace('"','')
                    comments_count = None
                    likes_count = None
                    title = ''
                    if(post.get('comments') != None):
                        comments_count = post.get('comments').get('count')
                    if(post.get('likes') != None):
                        likes_count = post.get('likes').get('count')
                    # Do the DB part here
                    cursor.execute("""SELECT InsertPost(%s, %s, %s, %s, %s, %s)""", (author_name, author_id, message, likes_count, comments_count, post_id))
                    code = cursor.fetchone()
                    # code[0] indicates the number of affected rows, if its 1 -> successful insert, if not the post already exists in thr Db
                    if(code[0] == 1 and post.get('link') !=  None):
                        link = post.get('link').encode('ascii','ignore')
                        if(post.get('name') != None):
                            title = controlchar_regex.sub(' ',post.get('name').encode('ascii','ignore').replace('"',''))
                        if(post.get('description') != None):
                            description = post.get('description').encode('ascii','ignore').replace('"','')
                            description = controlchar_regex.sub(' ',description) + ' - ' + author_name
                        else:
                            description = controlchar_regex.sub(' ',message) + ' - ' + author_name
                
                        # Build the JSON
                        values = '{"url": "'+link+'" , "list":"'+config.get('kippt','listuri')+'", "title":"'+title+'", "notes":"'+description+ '"}'
                        r = self.post_to_kippt(values)
                        self.post_link(r, post_id)

                    elif(code[0] == 1):
                       
                       # make this regex better if you want
                       try:
                           description = post.get('message').replace('"','')
                           description = controlchar_regex.sub(' ',description)
                           urls =  re.findall("(?P<url>https?://[^\s]+)", description)
                           for url in urls:
                               description = description.replace(url, '')
                           description = description  + ' - ' + author_name

                           for url in urls:
                               # Build the JSON
                               values = '{"url": "'+url+'" , "list": "'+config.get('kippt','listuri')+'", "notes":"'+description+'"}' 
                               r = self.post_to_kippt(values)
                               self.post_link(r, post_id)
                       except Exception, err:
                           logging.error(str(datetime.now())+" "+str(err))
                           traceback.print_exc(file = open(config.get('logging','errorlog'),'a'))
            except Exception, err:
                print 'Some error'
                logging.error(str(datetime.now())+" "+str(err))
                traceback.print_exc(file = open(config.get('logging','errorlog'),'a'))
        print "Archiving Complete!"
        logging.info(str(datetime.now())+' Archiving Complete for page: '+group_url)

    def post_to_kippt(self, values):
        print values
        config = self.config
        req = urllib2.Request(config.get('kippt','url'),values)
        req.add_header('X-Kippt-Username', config.get('kippt','username'))
        req.add_header('X-Kippt-API-Token', config.get('kippt','apitoken'))
        r = urllib2.urlopen(req)
        return r.read()                                                                   

    def post_link(self, response, post_id):
        cursor = self.cursor
        resp_data = json.loads(response)
        cursor.execute("""SELECT InsertLink(%s, %s, %s, %s) """,(resp_data.get('url'),resp_data.get('title'), resp_data.get('notes'), post_id ))
