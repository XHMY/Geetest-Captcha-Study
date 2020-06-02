# -*- coding: utf-8 -*-
"""
Created on Sun May 31 18:05:36 2020

@author: 28446
"""
import json
import requests

#点选
response = requests.get('https://www.geetest.com/demo/gt/register-phrase').text
response=json.loads(response)
old_challenge = response['challenge']
gt=response["gt"]


headers={
'Host': 'api.geetest.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
'Referer': 'https://ics.autohome.com.cn/passport/',
    }

img_u="https://static.geetest.com"
u_reset="https://api.geetest.com/reset.php?gt={}&challenge={}"
u_ajax="https://api.geetest.com/ajax.php?gt={}&challenge={}"
u_get_first="https://api.geetest.com/get.php?is_next=true&gt={}&challenge={}"
u_refresh_start="https://api.geetest.com/refresh.php?gt={}&challenge={}"




#链接存放文件名（当前目录）自定义修改
cnt=0
with open('image_url.txt','a',encoding='utf-8') as f:
    while True:
        reset_txt=requests.get(u_reset.format(gt,old_challenge),headers=headers).text
        reset_dict=json.loads(reset_txt.split('(')[1][:-1])
        new_challenge=reset_dict["data"]["challenge"]
        old_challenge=new_challenge
        ajax_txt=requests.get(u_ajax.format(gt,new_challenge),headers=headers).text
        stat=json.loads(ajax_txt.split('(')[1][:-1])["status"]
        if stat!="success":
            print(1)
            break
        get_first_txt=requests.get(u_get_first.format(gt,new_challenge),headers=headers).text
        get_first_dict=json.loads(get_first_txt.split('(')[1][:-1])
        if get_first_dict["status"]!="success":
            print(2)
            break
        u_img=img_u+get_first_dict["data"]["pic"]
        f.write(u_img+'\n')
        cnt+=1
        print(cnt,end=",")
        for i in range(5):
            u_refresh=u_refresh_start.format(gt,new_challenge)
            refresh_txt=requests.get(u_refresh,headers=headers).text
            refresh_dict=json.loads(refresh_txt.split('(')[1][:-1])
            if get_first_dict["status"]!="success":
                print(3)
                break
            u_img=img_u+refresh_dict["data"]["pic"]
            f.write(u_img+'\n')
            cnt+=1
            print(cnt,end=",")
        print()
f.close()