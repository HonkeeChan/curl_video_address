import socket,sys
import re
from thread import *

listening_port = 8083
max_conn = 100
buffer_size = 8192
video_url = []
video_suffix = ['mp4', 'flv', 'sfw']
#pattern = re.compile('.*[mp4 | flv | swf]')

def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', listening_port))
        s.listen(max_conn)
        print "[*] Initializing Sockets ... Done"
        print "[*] Sockets Binded Successfully ..."
        print ("[*] Server Started Successfully [ %d ]\n" % (listening_port))
    except Exception, e:
        print "[*] Unable To Initialize Socket"
        sys.exit(2)

    while 1:
        try:
            conn, addr =  s.accept()
            # print '[*] socket accept addr: ' 
            # print addr
            data = conn.recv(buffer_size)
            start_new_thread(conn_string, (conn, data, addr))
        except KeyboardInterrupt:
            s.close()
            print "\n[*] Proxy Server Shutting Down"
            print "[*] Have a nice day"
            sys.exit(1)
    s.close()

def conn_string(conn, data, addr):
    try:
        
        first_line = data.split('\n')[0]
        #print first_line
        url = first_line.split(' ')[1]
        # I am not familiar with the regular expression, i give up using it...
        #if re.match(pattern, url):
        #    print '***************' + url

        # I found a video suffix in the url, i turn the var `found` on
        found = False
        for s in video_suffix:
            if url.find(s) != -1:
                print '***************' + url
                found = True
                print '************response*******************'
                print data
                break;
                
            # video_url.append(url)
        # Find The Position of ://
        http_pos = url.find('://')
        if(http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(':')

        webserver_pos = temp.find('/')
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if(port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]
        # print "proxy_server: %s: %s" % (webserver, port)
        proxy_server(webserver, port, conn, data, addr, found)
    except Exception, e:
        print e

# var `isVideo` is use to print the response corresponding to the video request..
# but i can't find the response header , so i give up using it
def proxy_server(webserver, port, conn, data, addr, isVideo):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        #print 'send data to webserver'
        s.send(data)
        #print 'wating for reply'
        while 1:
            reply = s.recv(buffer_size)
            # print 'receive webserver reply'
            if(len(reply) > 0):
                # print 'send to the client'
                # if(isVideo):
                #     print '************reply*************'
                #     print reply.split('\n')[::6]
                conn.send(reply)
                dar = float(len(reply))
                dar = float(dar /1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                #'Print A Custom message For Request Complete'
                # print "[*] Request Done: %s => %s <=" % (str(addr[0]), str(dar))
            else:
                break

        s.close()
        conn.close()
    except socket.error, (value, message):
        s.close()
        conn.close()
        sys.exit(1)

if __name__ == '__main__':
    start()
