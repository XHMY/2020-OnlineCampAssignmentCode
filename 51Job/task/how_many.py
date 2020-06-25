import json
with open("jobs_list.json") as fd:
    data = json.loads(fd.read())
sum = 0
key_sum = 0
for key in data:
    key_sum += 1
    sum += len(data[key])

print("总共爬取到{}条工作信息，共来自{}个公司".format(sum,key_sum))

