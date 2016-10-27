#coding=utf-8
import threading
from time import ctime,sleep


def music(func,func1):
    print func
    print func1
    for i in range(2):
        print "I was listening to %s. %s" %(func, i)
        sleep(1)

def move(func):
    for i in range(3):
        print "I was at the %s! %s" %(func, i)
        sleep(5)

def newMove(func):
    for i in range(5):
        print "I was at the %s! %s" %(func, i)
        sleep(5)

def newThread(func):
    print "in new thread fun"
    t = threading.Thread(target=newMove,args=(u'move in new thread fun',))
    t.start()
    sleep(20)
    print "new thread finish"


threads = []
t1 = threading.Thread(target=newThread, args=(u'move',))
threads.append(t1)
t2 = threading.Thread(target=music,args=(u'music arg1',u'music arg2'))
threads.append(t2)
t3 = threading.Thread(target=move,args=(u'move',))
threads.append(t3)


if __name__ == '__main__':
    # threads[2].setDaemon(True)
    for t in threads:
        # t.setDaemon(True)
        t.start()

    for i in range(len(threads)):
        t = threads[i]
        print "waiting for thread join" + str(i)
        t.join() # 
        print "join ok"


    print "all over %s" %ctime()