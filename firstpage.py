import urllib
import urllib2
import json
import ConfigParser
import sys

from fb_group_sync import FbGroupArchiver

def index():
    config = ConfigParser.ConfigParser()
    if(len(sys.argv)>2):
        group_url = sys.argv[2]
    elif(len(sys.argv)>1):
        config.read(sys.argv[1])
        group_url = config.get('group','url')
    else:
        print 'Usage: python batch_script.py [Config file name] [group page url(optional)]'
        return
    url = 'Not found yet'
    data = urllib2.urlopen(group_url).read()
    jsondata = json.loads(data)
    print 'Finding first page url - Long running process. Might take several minutes.'
    while(group_url is not None):
        data = urllib2.urlopen(group_url).read()
        jsondata = json.loads(data)
        if(jsondata.get('paging') != None):
            url = group_url
            group_url = jsondata.get('paging').get('next')
        else:
            return
    print url

if __name__ == "__main__":
    index()

