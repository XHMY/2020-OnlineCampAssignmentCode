import json
import os
import shutil
import zipfile
total_num = 237235
member_num = 15
session = 1
source_file_py = "jobs_list_page_scrape.py"
source_file_json = "company_list.json"

# task = {"ID": 1, "start": 0, "amount": 100}  # 1号成员从第0页开始爬取100页


def compress_file(zipfilename, dirname):      # zipfilename是压缩包名字，dirname是要打包的目录
    if os.path.isfile(dirname):
        with zipfile.ZipFile(zipfilename, 'w') as z:
            z.write(dirname)
    else:
        with zipfile.ZipFile(zipfilename, 'w') as z:
            for root, dirs, files in os.walk(dirname):
                for single_file in files:
                    if single_file != zipfilename:
                        filepath = os.path.join(root, single_file)
                        z.write(filepath)


for i in range(member_num - 1):
    task = {"ID": i,
            "start": int(total_num/member_num)*i,
            "amount": int(total_num/member_num)}
    json_str = json.dumps(task, ensure_ascii=False)
    path = "task/task_"+str(session)+"_"+str(i)+"/"
    if not os.path.exists(path):
        os.makedirs(path)
    shutil.copy(source_file_py, path)
    shutil.copy(source_file_json, path)
    with open(path+"task.json", 'w') as fd:
        fd.write(json_str)
    compress_file("task/task_"+str(session)+"_"+str(i)+".zip", path)

task = {"ID": member_num - 1,
        "start": int(total_num/member_num)*(member_num - 1),
        "amount": int(total_num/member_num) + total_num % member_num}
json_str = json.dumps(task, ensure_ascii=False)
path = "task/task_"+str(session)+"_"+str(member_num - 1)+"/"
if not os.path.exists(path):
    os.makedirs(path)
shutil.copy(source_file_py, path)
shutil.copy(source_file_json, path)
with open(path+"task.json", 'w') as fd:
    fd.write(json_str)
compress_file("task/task_"+str(session)+"_"+str(member_num - 1)+".zip", path)
