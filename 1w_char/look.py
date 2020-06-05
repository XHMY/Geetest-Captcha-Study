import json

char_3500 = set()
with open("1w_char/char_form_others/3500_lwh.txt",'r') as fd:
    for c in fd.read():
        if c >= u'\u4e00' and c <= u'\u9fa5':
            char_3500.add(c)

# print(len(char_3500))

char_list  = []
with open("1w_char/tc_api_data/char_set_95_v2.0.json",'r') as fd:
    char_list = json.loads(fd.read())

total = len(char_list)
du_num = 0
print(total)
for c in char_list:
    if c in char_3500:
        du_num+=1
    else:
        char_3500.add(c)

with open("1w_char/char_set_result{}.txt".format(len(char_3500)),'w') as fd:
    for c in char_3500:
        fd.write(c)


print("重复率: {:.3f}%".format((du_num/total)*100))

print(total - du_num)