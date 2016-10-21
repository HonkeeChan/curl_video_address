#encoding: utf8
import logging
import pcap
import dpkt
import threading
import os
import time
import uuid
import numpy as np
import json




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


def wrapDownloadURL(requrl):
    logger.debug("in downloadfile, " + requrl)
    if(requrl.find('?') != -1):
        requrl = requrl.split("?")[0] 
    if(requrl.find("http://") == -1):
        requrl = "http://" + requrl
    return requrl

def downloadFile(fileurl, storename):
    logger.info("strat download " + fileurl)
    os.system("curl -o download/" + storename + " " + fileurl)
    logger.info("finish download " + fileurl)
    
pc = pcap.pcap("enp5s0")    #注，参数可为网卡名，如eth0
#设置监听过滤器 HTTP请求的TCP头为GET 或者 HTTP
pc.setfilter('tcp[20:2]=0x4745 or tcp[20:2]=0x4854')    


downloadedURL = dict()
contactList = []

if __name__ == '__main__':
    print "starting capture"
    for ptime,pdata in pc:    #ptime为收到时间，pdata为收到数据
    #对抓到的以太网V2数据包(raw packet)进行解包

        p=dpkt.ethernet.Ethernet(pdata)
        if p.data.__class__.__name__=='IP':
            ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))
            
            if p.data.data.__class__.__name__=='TCP':
                if p.data.data.dport == 80:
                   
                    header = p.data.data.data # by gashero
                    headerArr = header.split('\r\n')
                    url = headerArr[0].split(' ')[1]
                    host = headerArr[1].split(' ')[1]
                    requestUrl = host + url
                    if requestUrl.find('.flv') != -1 or requestUrl.find('.mp4') != -1:
                        videoUrl = wrapDownloadURL(requestUrl)
                        # logger.info(videoUrl) 
                        if(not downloadedURL.has_key(videoUrl)):
                            logger.debug("never download this url: " + videoUrl)
                            nowTime = time.time()
                            fileName = str(nowTime) + "." + videoUrl.split(".")[-1]
                            downloadedURL[videoUrl] = (nowTime, fileName)
                            contactList.append(fileName)
                            t = threading.Thread(target=downloadFile,args=(videoUrl , fileName))
                            t.start()
                        f = open("download/list.txt", "w")
                        toWrite = ["file '" + item + "'\n" for item in contactList]
                        f.writelines(toWrite)
                        f.close()

                    # if requestUrl.find('.swf') != -1:
                    #     # print headerArr
                    #     logger.info(requestUrl) 




def splitHeader(headerStr):
    headerArr = headerStr.split('\r\n')
    if(len(headerArr) > 5):
        url = headerArr[0].split(' ')[1]
        host = ":".join(headerArr[1].split(':')[1:]).strip()
        userAgent = ":".join(headerArr[2].split(':')[1:]).strip()
        accept = ":".join(headerArr[3].split(':')[1:]).strip()
        acceptLanguage = ":".join(headerArr[4].split(':')[1:]).strip()
        # acceptEncoding = ":".join(headerArr[5].split(':')[1:]).strip()
        # referer = ":".join(headerArr[6].split(':')[1:]).strip()
        # connection = ":".join(headerArr[5].split(':')[1:]).strip()



