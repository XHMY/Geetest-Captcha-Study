import cv2
import os
import numpy as np


def img_cropped(filename):
    img = cv2.imread(filename)
    return img[344:384, 0:116]
    # cv2.imshow('image',cropped)
    # cv2.waitKey(0)
    # v2.destroyAllWindows()




imgs = []
for k in os.walk('imgs'):
    if(k[0] != 'imgs'):
        continue
    for filename in k[2]:
        if(filename[-4:] != '.jpg'):
            continue
        imgs.append(img_cropped("imgs/"+filename))


width = 4  # 设置张图片多少列
height = 100  # 设置每张图片多少行
img_blank_v = np.zeros((40,60,3), np.uint8)
img_blank_v.fill(255)
img_blank_h = np.zeros((40,width*(116+60),3), np.uint8)
img_blank_h.fill(255)
vImg = []
i = 0
while True:
    t_img = []
    for img in imgs[i:i+width]:
        t_img.append(img)
        t_img.append(img_blank_v)
    vImg.append(cv2.hconcat(t_img))
    i += width
    if(i+width > len(imgs)):
        if(i!=len(imgs)):
            t_img = []
            for img in imgs[i:len(imgs)]:
                t_img.append(img)
                t_img.append(img_blank_v)
            cv2.imwrite("imgs/final/0v.jpg", cv2.hconcat(t_img))
        break

hImg = []
i = 0
while True:
    t_img = []
    for img in vImg[i:i+height]:
        t_img.append(img)
        t_img.append(img_blank_h)
    hImg.append(cv2.vconcat(t_img))
    i += height
    if(i+height > len(vImg)):
        if(i!=len(vImg)):
            t_img = []
            for img in vImg[i:len(vImg)]:
                t_img.append(img)
                t_img.append(img_blank_h)
            cv2.imwrite("imgs/final/0h.jpg", cv2.vconcat(t_img))
        break

i = 1
for img in hImg:
    cv2.imwrite("imgs/final/{}.jpg".format(i), img)
    i += 1
