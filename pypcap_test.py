#encoding: utf8
import pcap
import dpkt
pc=pcap.pcap("以太网")    #注，参数可为网卡名，如eth0
#设置监听过滤器 HTTP请求的TCP头为GET 或者 HTTP
pc.setfilter('tcp[20:2]=0x4745 or tcp[20:2]=0x4854')    

print "starting capture"
for ptime,pdata in pc:    #ptime为收到时间，pdata为收到数据
#对抓到的以太网V2数据包(raw packet)进行解包

    p=dpkt.ethernet.Ethernet(pdata)
    if p.data.__class__.__name__=='IP':
        ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))
        print ip
        if p.data.data.__class__.__name__=='TCP':
            if p.data.data.dport==80:
                header = p.data.data.data # by gashero
                headerArr = header.split('\r\n')
                url = headerArr[0].split(' ')[1]
                host = headerArr[1].split(' ')[1]
                requestUrl = host + url
                print requestUrl
                if requestUrl.find('.flv') != -1:
                    # print headerArr
                    print ptime
                    print requestUrl
            
