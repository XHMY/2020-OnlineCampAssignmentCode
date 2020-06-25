import json
with open("task.json", 'r') as fd:
    task = json.loads(fd.read())

with open("company_pageURL_list.json", 'r') as fd:
    url_list = json.loads(fd.read())

for i in range(task[1], task[2]):
    print(url_list[i])
    # do something to the url


with open("company_list" + str(task[0]) + ".json", 'w') as fd:
    fd.write(json_str)
