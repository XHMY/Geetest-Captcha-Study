import os

def no_dupi_set(filename):
    with open(filename,'r') as fd:
        data = set(fd.readlines())
    return data


all_data = []

for k in os.walk('res'):
    for filename in k[2]:
        all_data.append(no_dupi_set("res/"+filename))

bef_len = 0
final_data = set()
for data in all_data:
    bef_len += len(data)
    final_data.update(data)

print("不同文件汇总后数据有效率为 {:.3f}%".format((len(final_data)/bef_len)*100))
print("{} -> {}".format(bef_len,len(final_data)))

import json
with open("final_result.json",'w') as fd:
    fd.write(json.dumps(list(final_data)))