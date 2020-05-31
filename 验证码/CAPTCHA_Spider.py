from selenium.webdriver import Chrome
import time
import requests
import threading
from lxml.etree import HTML
import re

from wget import download


# 传入参数为selenium的浏览器（状态为第一次进入页面），需要触发一次显示验证码并返回对应的图片地址


def first_click(web):
    time.sleep(1)
    web.execute_script(
        "document.getElementsByClassName('geetest_radar_tip')[0].click()")
    time.sleep(1)
    ele = web.find_elements_by_xpath('//*[@class="geetest_item_img"]')
    for i in ele:
        pic_url = i.get_attribute('src').split('?')[0]
    return pic_url


# 传入参数为selenium的浏览器（状态为触发5次之后的重试），需要触发一次显示验证码并返回对应的图片地址


def retry_clikc(web):
    # time.sleep(1)
    web.execute_script(
        "document.getElementsByClassName('geetest_refresh')[0].click()")
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


def get_challenge(web, i):
    # i=0#i为点击重试次数
    # i=i+1
    selector = HTML(web.page_source)
    selector_challenge = selector.xpath(
        '/html/head/script[4+10*{}]/@src'.format(i))[0]
    challenge = selector_challenge.split('=')[3].split('&')[0]
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
        print("\nthread " + str(threadID) + " 开始下载 " + cur[0].split('/')[-1])
        img_path = 'imgs/{}'.format(cur.split('/')[-1])
        try:
            download(cur, img_path)
        except Exception as e:
            print("\n" + str(e))
            error_img_list.append([cur, str(e)])


error_img_list = []
picurlQ = []
picSet = {}
finish = False


def run_scrape():
    task_num = 10
    cnt = 0
    cnt_c = 0
    web = Chrome()  # 使用Chrome打开，WebDrive放置在bin目录下因此不需要指定路径
    web.get("https://ics.autohome.com.cn/passport/")
    # page = web.page_source # 获取网页源代码
    picurlQ.append(first_click(web))
    gt = get_gt(web)
    challenge = get_challenge(web, cnt_c)

    while cnt < task_num:
        if cnt % 5 and cnt != 0:
            picurlQ.append(retry_clikc(web))
            challenge = get_challenge(web, cnt_c)
            cnt_c += 1
            cnt += 1
        url = "https://api.geetest.com/refresh.php?gt={}&challenge={}&lang=zh-cn&type=click&callback=geetest_{}".format(
            gt, challenge, int(round(time.time() * 1000)))
        data = requests.get(url).text
        picurlQ.append("https://static.geetest.com" + re.match(r"pic\": \"(.+?)\"", data).group(1))
        cnt += 1


run_scrape()
