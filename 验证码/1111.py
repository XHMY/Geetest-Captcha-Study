from selenium.webdriver import Chrome
from lxml.etree import HTML
import time

def openUrl():
    web=Chrome()
    web.get('https://ics.autohome.com.cn/passport/')
    time.sleep(1)
    return web
web = openUrl()

def get_gt(web):
    ele=web.find_element_by_xpath("//*[@charset='UTF-8']")
    gt=ele.get_attribute('src').split('=')[1].split('&')[0]
    return gt
print(get_gt(web)) 

def get_challenge(web):
    i=0#i为点击重试次数
    # i=i+1
    selector = HTML(web.page_source)
    selector_challenge=selector.xpath('/html/head/script[4+10*{}]/@src'.format(i))[0]
    challenge=selector_challenge.split('=')[3].split('&')[0]
    return challenge
# web.close()
print(get_challenge(web))