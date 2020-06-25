import json
import os

num = 30

with open("jobs_url_list.json", 'r') as fd:
    data = json.loads(fd.read())

single = int(len(data)/num)
sin_data = []
for i in range(len(data)):
    # if(i ==len(data)-1):
    #     raise Exception
    if(i % single == 0 or i == len(data)- 1):

        if(i != 0):
            path = "task3/task_"+str(int(i/single))+"/"
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path+"jobs_url_list.json", 'w') as fd:
                fd.write(json.dumps(sin_data))
            print("{}: len={}".format(int(i/single), len(sin_data)))
        sin_data = []
    sin_data.append(data[i])
