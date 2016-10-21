#encoding: utf8

import sys
import requests
import pyquery

if __name__ == '__main__':
    if len(sys.argv) > 1:
        page = requests.get(sys.argv[1])
        doc = pyquery.PyQuery(page.content)
        player = doc("#player")
        print 'video url: ', player.attr("href")
    else:
        print "useage: python get_video_from_xjtu.py http://the.video.webpage"

