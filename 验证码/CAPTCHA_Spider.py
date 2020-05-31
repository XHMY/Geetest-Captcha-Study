from selenium.webdriver import Chrome
import time
import requests
import threading
from lxml.etree import HTML
import re

from wget import download


# 传入参数为selenium的浏览器（状态为第一次进入页面），需要触发一次显示验证码并返回对应的图片地址


def first_click(web):
    time.sleep(2.5)
    web.execute_script(
        "document.getElementsByClassName('geetest_radar_tip')[0].click()")
    time.sleep(2)
    ele = web.find_elements_by_xpath('//*[@class="geetest_item_img"]')
    for i in ele:
        pic_url = i.get_attribute('src').split('?')[0]
    return pic_url


# 传入参数为selenium的浏览器（状态为触发5次之后的重试），需要触发一次显示验证码并返回对应的图片地址


def retry_clikc(web):
    web.execute_script(
        "document.getElementsByClassName('geetest_refresh')[0].click()")
    time.sleep(1)
    web.execute_script(
        "document.getElementsByClassName('geetest_reset_tip_content')[0].click()")
    time.sleep(1)
    ele = web.find_elements_by_xpath('//*[@class="geetest_item_img"]')
    for i in ele:
        pic_url = i.get_attribute('src').split('?')[0]
    return pic_url


# 传入参数为selenium的浏览器，需要在页面中找到gt并返回


def get_gt(web):
    ele = web.find_element_by_xpath("//*[@charset='UTF-8']")
    gt = ele.get_attribute('src').split('=')[1].split('&')[0]
    return gt


# 传入参数为selenium的浏览器（状态为显示第一张验证码完后），需要在页面中找到challenge并返回


def get_challenge(web):
    # i=0#i为点击重试次数
    # i=i+1
    selector = HTML(web.page_source)
    # 定位到正确的包含Challenge的位置
    selector_challenge = str(selector.xpath('/html/head/script[.]/@src')[-1])
    challenge = re.search(r"&challenge=(.+?)&", selector_challenge).group(1)
    return challenge


class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("开始线程：" + self.name)
        download_image(self.threadID)
        print("退出线程：" + self.name)


def download_image(threadID):
    while not finish:
        if (len(picurlQ) == 0):
            time.sleep(1)
            continue
        cur = picurlQ.pop()
        # print("\nthread " + str(threadID) + " 开始下载 " + cur[0].split('/')[-1])
        img_path = 'imgs/{}'.format(cur.split('/')[-1])
        try:
            download(cur, img_path)
        except Exception as e:
            print("\n" + str(e))
            error_img_list.append([cur, str(e)])


error_img_list = []  # 错误列表
# picurlQ = []  # 下载图片任务队列
picSet = set()  # 记录所有下载过的图片的集合
# finish = False  # 完成标示


def run_scrape():

    task_num = 30  # 爬多少个验证码停止（包括重复的）
    cnt = 0  # 用于记录一部分总数
    cnt_c = 0  # 用于记录重试次数
    du_cnt = 0  # 用于记录重复的次数
    # thread_num = 5  # 下载的线程数
    # down_thread = []  # 线程list

    web = Chrome()  # 使用Chrome打开，WebDrive放置在bin目录下因此不需要指定路径
    web.get("https://ics.autohome.com.cn/passport/")
    t_url = first_click(web)# 初始页面第一次点击
    # picurlQ.append(t_url) 
    picSet.add(t_url)
    fd.write(t_url + '\n')
    gt = get_gt(web) # 获取gt值（从头到位不会变）
    challenge = get_challenge(web) # 获取第一个challenge值

    # 开启用于下载图片的线程
    # for i in range(thread_num):
    #     down_thread.append(myThread(i))
    #     down_thread[i].start()

    # 主爬取循环
    while cnt + cnt_c < task_num:
        # 每5次需要点击重试
        if cnt % 5 == 0 and cnt != 0:
            cnt_c += 1
            t_url = retry_clikc(web) # 点击重试
            # 如果这个url已经在里面，就跳过
            if t_url in picSet:
                du_cnt += 1
                print("\n检测到重复链接，当前总计重复{}张，本次任务重复率 {:.2}%".format(
                    du_cnt, (cnt+cnt_c)/du_cnt*100))
                continue
            challenge = get_challenge(web) # 获取challenge
            picSet.add(t_url)
            fd.write(t_url + '\n')
            # picurlQ.append(t_url)
            print("\n已爬取 {} 个验证码链接".format(cnt + cnt_c))
        url = "https://api.geetest.com/refresh.php?gt={}&challenge={}&lang=zh-cn&type=click&callback=geetest_{}".format(
            gt, challenge, int(round(time.time() * 1000)))
        data = requests.get(url).text
        t_url = "https://static.geetest.com" + \
            re.search(r"pic\": \"(.+?)\"", data).group(1)
        cnt += 1
        if t_url in picSet:
            du_cnt += 1
            print("\n检测到重复链接，当前总计重复{}张，本次任务重复率 {:.2}%".format(
                du_cnt, (cnt+cnt_c)/du_cnt*100))
            continue
        picSet.add(t_url)
        fd.write(t_url + '\n')
        # picurlQ.append(t_url)
    # finish = True
    # for i in range(thread_num):
    #     down_thread[i].join()
    web.close()


# 打开用于记录URL的文件
fd = open("image_url.txt",'a+')

# 把所有文件中已经读到的添加到set中
line = fd.readline()
while line: 
    picSet.add(line)
    line = f.readline()

# 开始运行爬虫
run_scrape()

# 关闭文件
fd.close()

