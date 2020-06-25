import threading
import time

exitFlag = 0
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开始线程：" + self.name)
        print_time(self.name)
        print("退出线程：" + self.name)


def print_time(threadName):
    while len(my_list) != 0:
        cur = my_list.pop()
        print(threadName + "  " + str(cur))


# 创建新线程
thread1 = myThread(1, "Thread-1")
thread2 = myThread(2, "Thread-2")

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("退出主线程")
