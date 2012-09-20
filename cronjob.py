import sys

from fb_group_sync import FbGroupArchiver

if len(sys.argv < 2):
    print 'Pass config file as command line arg'
else
    FbGroupArchiver(sys.argv[1]).process_data()
