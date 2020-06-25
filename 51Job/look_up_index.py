import json

with open("company_list.json", 'r', encoding='utf-8') as fd:
    data = json.loads(fd.read())

lookup = "华润万家有限公司-上海公司"

for i in range(len(data)):
    if data[i][0] == lookup:
        print(i)
