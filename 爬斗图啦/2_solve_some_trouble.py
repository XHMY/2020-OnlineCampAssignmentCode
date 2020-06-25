import json

with open("爬斗图啦/Pic_URL1_1627.json", 'r') as fd:
    data1 = json.loads(fd.read())
with open("爬斗图啦/Pic_URL1600_3444.json", 'r') as fd:
    data2 = json.loads(fd.read())

data = []
cnt_set = set()


def solve(s_data):
    for i in range(len(s_data)):
        if len(s_data[i][0]) == 0:
            print("Empty" + str(i))
            continue
        for j in range(len(s_data[i][0])):
            if s_data[i][0][j] in cnt_set:
                continue
            cnt_set.add(s_data[i][0][j])
            data.append([s_data[i][0][j], s_data[i][1][j]])


solve(data1)
solve(data2)

print("We got " + str(len(data))+" url")
json_str = json.dumps(data, ensure_ascii=False)
filename = '爬斗图啦/Pic_URL.json'
with open(filename, 'w') as fd:
    fd.write(json_str)
