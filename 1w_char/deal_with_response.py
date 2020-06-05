import json
import cv2


def img_cropped(filename, x1,x2,y1,y2):
    img = cv2.imread(filename)
    # return img[y1:y2, x1:x2]
    cropped = img[y1:y2, x1:x2]
    cv2.imshow('image',cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

with open("1w_char/tc_api_data/10w_API_response.json", 'r') as fd:
    data = json.loads(fd.read())

# text_97  = []
char_set = set()
invalid_char_set = set()
total = 0
valid = 0

for pic in data:
    for text in pic["TextDetections"]:
        total+=1
        if text["Confidence"]>=95:
            valid+=1
            for c in text["DetectedText"]:
                if c >= u'\u4e00' and c <= u'\u9fa5':
                    char_set.add(c)
            # text_97.append(text["DetectedText"])
        elif text["Confidence"]<60:
            for c in text["DetectedText"]:
                if c >= u'\u4e00' and c <= u'\u9fa5':
                    invalid_char_set.add(c)

print("收集到不重复的汉字个数为: {}".format(len(char_set)))
print("API检测达标率为: {:.3f}%".format((valid/total)*100))
with open("1w_char/tc_api_data/char_set_95_v2.0.json",'w') as fd:
    # for c in char_set:
    #     fd.write(c)
    fd.write(json.dumps(list(char_set),ensure_ascii=False))
with open("1w_char/tc_api_data/inva_char_set_95_v1.0.json",'w') as fd:
    fd.write(json.dumps(list(invalid_char_set),ensure_ascii=False))


# cur = data[0]["TextDetections"][0]["Polygon"]
# img_cropped("imgs/final/1.jpg",cur[0]["X"],cur[1]["X"],cur[1]["Y"],cur[2]["Y"])