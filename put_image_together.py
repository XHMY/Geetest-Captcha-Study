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
    for filename in k[2]:
        if(filename[-4:]!='.jpg'):
            continue
        imgs.append(img_cropped("imgs/"+filename)) 


width = 5
height = 20
vImg = []  
i = 0
while True:
    vImg.append(cv2.hconcat(imgs[i:i+width]))
    i+=width
    if(i+width>len(imgs)):
        break

hImg = []
i=0
while True:
    hImg.append(cv2.vconcat(vImg[i:i+height]))
    i+=height
    if(i+height>len(vImg)):
        break

i=0
for img in hImg:
    cv2.imwrite("imgs/final/{}.jpg".format(i), img)
    i+=1

    
