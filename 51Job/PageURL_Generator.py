import json
url_list = []
for i in range(1, 2374):
    url_list.append("https://company.51job.com/p" + str(i)+"/")
json_str = json.dumps(url_list, ensure_ascii=False)
with open("company_pageURL_list.json", 'w') as fd:
    fd.write(json_str)
