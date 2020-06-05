import cv2
import os
import numpy as np

def img_cropped(filename):
    img = cv2.imread(filename)
    return img[344:384, 0:116]
    # cv2.imshow('image',cropped)
    # cv2.waitKey(0)
    # v2.destroyAllWindows()


def do_the_work(imgs):
    vImg = []
    while len(imgs)!=0:
        t_img = []
        for t in range(width):
            t_img.append(imgs.pop())
            t_img.append(img_blank_v)
        vImg.append(cv2.hconcat(t_img))

    # hImg = []
    
    while len(vImg)!=0:
        t_img = []
        for t in range(height):
            t_img.append(vImg.pop())
            t_img.append(img_blank_h)
        cv2.imwrite("final/{}.jpg".format(cnt+1), cv2.vconcat(t_img))
        

cnt = 0
width = 4  # 设置张图片多少列
height = 100  # 设置每张图片多少行
path = "H:/imgs_have/"
m=0
img_blank_v = np.zeros((40,60,3), np.uint8)
img_blank_v.fill(255)
img_blank_h = np.zeros((40,width*(116+60),3), np.uint8)
img_blank_h.fill(255)
imgs = []
# 假设图片全部在当前目录imgs文件夹中
for k in os.walk('H:/imgs_have'):
    if(k[0] != 'H:/imgs_have'):
        continue
    for filename in k[2]:
        if(filename[-4:] != '.jpg'):
            continue
        imgs.append(img_cropped(path+filename))
        m+=1
        print('\r{}--'.format(m),end='')
        if(len(imgs)==width*height):
            do_the_work(imgs)
            cnt+=1
            print(cnt)
        

