import cv2
import os


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


width = 5  # 设置张图片多少列
height = 20  # 设置每张图片多少行
vImg = []
i = 0
while True:
    vImg.append(cv2.hconcat(imgs[i:i+width]))
    i += width
    if(i+width > len(imgs)):
        cv2.imwrite("imgs/final/0v.jpg", cv2.hconcat(imgs[i:len(imgs)]))
        break

hImg = []
i = 0
while True:
    hImg.append(cv2.vconcat(vImg[i:i+height]))
    i += height
    if(i+height > len(vImg)):
        cv2.imwrite("imgs/final/0h.jpg", cv2.vconcat(vImg[i:len(vImg)]))
        break

i = 1
for img in hImg:
    cv2.imwrite("imgs/final/{}.jpg".format(i), img)
    i += 1
