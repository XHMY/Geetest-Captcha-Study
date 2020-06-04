import json
import threading
import os
from wget import download

class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("开始线程:" + self.name)
        download_image(self.threadID)
        print("退出线程:" + self.name)


def download_image(threadID):
    while len(task_q)!=0:
        cur = task_q.pop()
        print("\nthread " + str(threadID) + " 开始下载 " + cur.split('/')[-1])
        img_path = 'imgs/{}'.format(cur.split('/')[-1])
        try:
            download(cur, img_path)
        except Exception as e:
            print("\n" + str(e))
            error_img_list.append([cur, str(e)])

error_img_list = []
thread_num = 10  # 下载的线程数
down_thread = []  # 线程lis
img_url_list= json.loads(open('Spider/img_url_result.json','r',encoding='utf-8').read())
task_q = []

for i in range(10000,30000):
    task_q.append(img_url_list[i][:-1])

# 开启用于下载图片的线程
for i in range(thread_num):
    down_thread.append(myThread(i))
    down_thread[i].start()
