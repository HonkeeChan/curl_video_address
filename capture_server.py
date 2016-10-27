# encoding: utf8
import tornado.ioloop
import tornado.web
import tornado.escape
import Queue
import threading
import time
import requests
import pyquery
import logging
from capture import TrafficCapture 
import os


logger = logging.getLogger("curl_video")
logger.setLevel(logging.DEBUG)      
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler("curl_video.log")
fh.setLevel(logging.DEBUG)       
# 再创建一个handler，用于输出到控制台                                   
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)     
# 定义handler的输出格式
# format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(mess
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)


START_PROGRESS = 1
IN_PROGRESS = 2
FINISH = 0

urlQueue = Queue.Queue()

"""
post request just push the different url into the 
urlQueue and resultDict and then return

the main thread(capture thread), will get url from the urlQueue, 
when capture finish the main thread will fill the resultDict.
when the post request come next time, it will get the result
"""



class MainHandler(tornado.web.RequestHandler):
  

    def get(self):
        time.sleep(1)
        self.write("hello world")

    def post(self):
        global resultDict
        ret = {}
        print "result dict: ", resultDict
        videoUrl = self.get_argument("url", default=None)
        if(videoUrl):
            if(resultDict.has_key(videoUrl)):
                if resultDict[videoUrl]:
                    print("finish get video, " + videoUrl)
                    ret["msg"] = "finish"
                    ret["code"] = FINISH
                    ret["data"] = resultDict[videoUrl]
                    del resultDict[videoUrl]
                else:
                    print("get video in progress, " + videoUrl)
                    ret["msg"] = "in progress"
                    ret["code"] = IN_PROGRESS

            else:
                print("get video in progress, " + videoUrl)
                urlQueue.put(videoUrl)
                resultDict[videoUrl] = None
                ret["msg"] = "in progress"
                ret["code"] = IN_PROGRESS
        else:
            ret["code"] = -1
            ret["msg"] = "参数错误"

        respon_json = tornado.escape.json_encode(ret)
        self.write(respon_json)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

def tornadoThread():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

def wrapDownloadURL(requrl):
    if(requrl.find('?') != -1):
        requrl = requrl.split("?")[0] 
    if(requrl.find("http://") == -1):
        requrl = "http://" + requrl
    return requrl

def openVideo(videoUrl):
    print 'open ' + videoUrl
    os.system("xvfb-run /home/honkee/slimerjs-0.10.1/slimerjs open_url.js " + videoUrl)
    print "browser exit"
    tc.stop()
    # make a http get request, let the capture thread return
    time.sleep(2)
    a = requests.get("http://www.baidu.com")

if __name__ == "__main__":
    logging.debug("start tornado thread")
    t = threading.Thread(target=tornadoThread)
    t.start()

    global tc
    global resultDict
    resultDict = {}
    tc = None
    while True:
        print("in while")
        if urlQueue.qsize() > 0:
            urlOri = urlQueue.get()
            print("get url from queue " + urlOri)
            print("que size: " + str(urlQueue.qsize()))
            url = wrapDownloadURL(urlOri)
            res = requests.get(url)
            doc = pyquery.PyQuery(res.content)
            title = doc("title").text()
            tc = TrafficCapture("enp5s0", title, "curl_video")
            browser = threading.Thread(target=openVideo, args= (url,))
            browser.start()
            tc.start()
            videoDownloadUrlArr = tc.getDownloadUrls()
            resultDict[urlOri] = videoDownloadUrlArr
        else:
            time.sleep(10)




    print 'never get here'
    
    
