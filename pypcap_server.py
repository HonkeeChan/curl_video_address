# encoding: utf8
import tornado.ioloop
import tornado.web
import tornado.escape
import Queue
import threading
import thread
import time
import pcap
import dpkt


urlQueue = Queue.Queue()
startTime = None
videoUrl = None
resultDict = {}


class captureThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global videoUrl
        global resultDict

    def run(self):
        pc = pcap.pcap('eth1')    # 注，参数可为网卡名，如eth0
        # 设置监听过滤器 HTTP请求的TCP头为GET 或者 HTTP
        pc.setfilter('tcp[20:2]=0x4745 or tcp[20:2]=0x4854')

        print "starting capture ..."
        for ptime, pdata in pc:    # ptime为收到时间，pdata为收到数据
            # 对抓到的以太网V2数据包(raw packet)进行解包
            if not videoUrl:
                continue
            startTime = ptime
            resultDict[videoUrl] = []
            p = dpkt.ethernet.Ethernet(pdata)
            if p.data.__class__.__name__ == 'IP':
                # ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))
                if p.data.data.__class__.__name__ == 'TCP':
                    if p.data.data.dport == 80:
                        header = p.data.data.data   # by gashero
                        headerArr = header.split('\r\n')
                        url = headerArr[0].split(' ')[1]
                        host = headerArr[1].split(' ')[1]
                        requestUrl = host + url
                        if requestUrl.find('.flv') != -1:
                            resultDict[videoUrl].append(requestUrl)
            if ptime - startTime > 100:
                videoUrl = None
                startTime = None


class MainHandler(tornado.web.RequestHandler):
    def __init__(self):
        tornado.web.RequestHandler.__init__(self)
        global videoUrl
        global resultDict

    def get(self):
        time.sleep(1)
        self.write("hello world")

    def post(self):
        videoUrl = self.get_argument("url", default=None)
        ret = {
            "code": -1,
            "data": "参数错误"
        }
        ret["data"] = resultDict[videoUrl]
        respon_json = tornado.escape.json_encode(ret)
        self.write(respon_json)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    thread.start_new_thread(tornado.ioloop.IOLoop.current().start())
    print "hello"
    time.sleep(1000)
    
    
