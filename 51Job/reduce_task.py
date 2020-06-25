import json
member_num = 15
session = 0
source_file_json_prefix = "jobs_list"
total = {}
for i in range(member_num):
    with open("task/"+source_file_json_prefix+str(i)+".json", 'r', encoding='utf-8') as fd:
        total.update(json.loads(fd.read()))

with open("task/" + source_file_json_prefix + ".json", 'w', encoding='utf-8') as fd:
    fd.write(json.dumps(total, ensure_ascii=False))

