# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 00:23:38 2020

@author: Spirit H
"""


import json
import re


'''以置信度分类'''
def judge(i , j , region , x):
    if data[i]['TextDetections'][j]['Confidence'] > 100-region*x:
        with open('Confidence_{}~{}.txt'.format(100-region*x+5 , 100-region*x+1) , 'a' , 
                  encoding = 'utf-8') as f:
            f.write(data[i]['TextDetections'][j]['DetectedText'])
            f.write('\n')
    else:
        judge(i , j , region , x+1)

'''计算命中率'''
def check_percent(region , x):
    try:
        with open('Confidence_{}~{}.txt'.format(100-region*x+5 , 100-region*x+1) , 'r' , 
                  encoding = 'utf-8') as f:
            words = f.read()
        words = re.findall('\w' , words) # 得到该文件所有字
        #print(words)
        s = 0
        for i in words:
            if i in words_3500:
                s = s + 1
        #print(s)
        #print(len(words))
        result = s/len(words)
        #print(result)
        print('置信度在{}~{}间的命中率为{}'.format(100-region*x+5 , 100-region*x+1 , result))
        #print('\n')
        check_percent(5 , x + 1)
    except Exception:
        #print('{} , 该文件不存在'.format('Confidence_{}~{}.txt'.format(100-region*x+5 , 100-region*x+1)))
        print('done')

'''解析json并新建为txt方便查询'''
with open('3w_API_response.json' , 'r' , encoding = 'utf-8') as f:
    data = f.read()
    data = json.loads(data)
list_num = len(data)
#print('the list has {} elements'.format(str(list_num)))

with open('3w_API_response.txt' , 'w' , encoding = 'utf-8') as f:
    f.write(str(data))
'''统计'''
num = 0
for i in range(len(data)):
    num = num + len(data[i]['TextDetections'])
#print('total texts: ' + str(num))

''''''
suc_num = 1
for i in range(list_num):
    for j in range(len(data[i]['TextDetections'])):
        print('{} ...'.format(suc_num) , end = '')
        suc_num = suc_num + 1
        judge(i , j , 5 , 1)
        print('done')
    #break

'''获得各区间文字在3500的命中率'''
with open('3500.txt' , 'r' , encoding = 'utf-8') as f:
    words_3500 = f.read()
words_3500 = re.findall('\w' , words_3500)
check_percent(5 , 1)


print('the list has {} elements'.format(str(list_num)))
print('total texts: ' + str(num))
print('analysing...done')

#print(type(data[0]['TextDetections'][0]['Confidence']))
    #print(len(data[i]['TextDetections']))
#print(data[0]['TextDetections'][0]['Confidence']) #

