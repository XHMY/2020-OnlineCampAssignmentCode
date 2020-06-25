import json
import re

result = {}

re_week = r"jq_matchindex_[0-9]+_td\\\">(.*?)\<"
re_league = r"status=\\\"0\\\">(.*?)\<"
re_matchtime = r"jq_league_matchTime_[0-9]+\\\">(.*?)\<"
re_hostteam = r"jq_match_hostteam_[0-9]+_span\\\">(.*?)\<"
re_guestteam = r"jq_match_guestteam_[0-9]+_span\\\">(.*?)\<"
re_score = r"class=\\\"wcbf_color\\\">(.*?)\<"
re_halfscore = r"\\r\\n\\t\\t\\t\\t<span class=\\\"red\\\">(.*?)\<"
re_letpoint = r"letPoint=\\\"(.*?)\\"
re_sp1 = r"jczq_xspf_gd':'(.*?)'"
re_sp2 = r"jczq_spf_gd':'(.*?)'"


def load_json():
    filename = '/Users/yokey/OneDrive/吉珠/Project/大一下线上工作室/code/爬竞彩足球/scrape_data.json'
    with open(filename, 'r') as fd:
        json_str = fd.read()
        source_data = json.loads(json_str)
        # print(source_data['2013-01-30']["0"])
    # print(data['2019-03-04']["1"])
    return source_data


def decode_single(date, response1, response_sp):
    result[date] = {}
    result[date]["week"] = []
    for match in re.finditer(re_week, response1):
        result[date]["week"].append(match.group(1))
    if len(result[date]["week"]) == 0:
        return False
    result[date]["league"] = []
    for match in re.finditer(re_league, response1):
        result[date]["league"].append(match.group(1))
    result[date]["matchtime"] = []
    for match in re.finditer(re_matchtime, response1):
        result[date]["matchtime"].append(match.group(1))
    result[date]["hostteam"] = []
    for match in re.finditer(re_hostteam, response1):
        result[date]["hostteam"].append(match.group(1))
    result[date]["guestteam"] = []
    for match in re.finditer(re_guestteam, response1):
        result[date]["guestteam"].append(match.group(1))
    result[date]["score"] = []
    for match in re.finditer(re_score, response1):
        result[date]["score"].append(match.group(1))
    result[date]["halfscore"] = []
    for match in re.finditer(re_halfscore, response1):
        result[date]["halfscore"].append(match.group(1))
    result[date]["letpoint"] = []
    for match in re.finditer(re_letpoint, response1):
        result[date]["letpoint"].append(match.group(1))
    result[date]["sp1"] = []
    for match in re.finditer(re_sp1, response_sp):
        result[date]["sp1"].append(match.group(1))
    if len(result[date]["sp1"]) == 0:
        result[date]["sp1"] = "---"
        result[date]["sp2"] = "---"
        return True
    result[date]["sp2"] = []
    for match in re.finditer(re_sp2, response_sp):
        result[date]["sp2"].append(match.group(1))
    return True


source_data = load_json()
for key in source_data:
    decode_single(key, source_data[key]["0"], source_data[key]["1"])
json_str = json.dumps(result, ensure_ascii=False)
filename = '/Users/yokey/OneDrive/吉珠/Project/大一下线上工作室/code/爬竞彩足球/result.json'
with open(filename, 'w') as fd:
    data = fd.write(json_str)
