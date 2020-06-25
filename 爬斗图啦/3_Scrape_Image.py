import json
import threading
from wget import download
from retrying import retry

filename = 'Pic_URL.json'
with open(filename, 'r') as fd:
    pic_list = json.loads(fd.read())

total_len = len(pic_list)


class myThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("开始线程：" + self.name)
        download_image(self.threadID)
        print("退出线程：" + self.name)


@retry(stop_max_attempt_number=3, wait_random_min=300, wait_random_max=1500, stop_max_delay=4000)
def single_download(url, img_path):
    download(url, img_path)


error_list = []


def download_image(threadID):
    while len(pic_list) != 0:
        cur = pic_list.pop()
        print("\nthread " + str(threadID) + " 开始下载 " + cur[0].split('/')[-1])
        img_path = '/Users/yokey/Downloads/imgs/{}'.format(
            cur[0].split('/')[-1])
        try:
            single_download(cur[0], img_path)
        except Exception as e:
            print("\n" + str(e))
            error_list.append(cur)


threads = []
thread_num = 5
for i in range(thread_num):
    threads.append(myThread(i))
    threads[i].start()

for i in range(thread_num):
    threads[i].join()
    print("线程" + str(i)+"已完成")

if len(error_list) != 0:
    print("总共有" + str(len(error_list))+"个文件下载失败，已输出到运行目录")
    json_str = json.dumps(error_list)
    with open("error_list.json", 'w') as fd:
        fd.write(json_str)
print("Finish")
