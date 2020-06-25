import threading
import requests
import datetime
import time
import json


class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        # print("开始线程：" + str(self.threadID))
        run_scrape(self.threadID)
        # print("退出线程：" + str(self.threadID))

# e_cnt = 0

def run_scrape(threadID):
    try:
        #print("线程{}发送请求".format(threadID))
        st = datetime.datetime.now()
        staus = requests.get("http://121.199.60.137:8888/",
                             timeout=10).status_code
        cur_t = (datetime.datetime.now() - st).microseconds / 1000000
        log.append([str(threadID), cur_t, str(staus)])
        # print("线程{} 耗时{}秒 status_code:{}".format(threadID, cur_t, staus))

    except Exception as e:
        # error_list.append(str(e))
        # e_cnt+=1
        print("线程{}响应遇到错误 {}".format(
            threadID, str(e)))
        log.append([str(threadID), (datetime.datetime.now() -
                                    st).microseconds / 1000000, str(e)])


thread = []
thread_num = 10000
log = []
# starttime = datetime.datetime.now()
for i in range(thread_num):
    thread.append(myThread(i))
    
for i in range(thread_num):
    thread[i].start()

for i in range(thread_num):
    thread[i].join()

print("程序运行完成，错误率{}%".format(e_cnt / thread_num))
# endtime = datetime.datetime.now()
# print("运行耗时 {} 秒".format((endtime - starttime).microseconds / 1000000))
# for i in range(task["start"], task["start"] + task["amount"]):
#     data = {}
#     data["标签"] = get_label(get_urls(job_list[i][6]))

# 将结果写入文件
with open("log.json", 'w', encoding='utf-8') as fd:
    fd.write(json.dumps(log, ensure_ascii=False))
