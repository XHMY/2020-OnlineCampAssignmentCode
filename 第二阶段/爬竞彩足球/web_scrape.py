import urllib.request as r
from urllib.error import HTTPError
import pandas as pd
import json
import time
from retrying import retry


@retry
def get_data(date):
    # time.sleep(1)
    d = date.strftime("%Y-%m-%d")
    data[d] = {}
    url = "https://live.aicai.com/jsbf/timelyscore!dynamicMatchDataForJczq.htm?dateTime=" + \
        str(d)
    da = r.urlopen(url).read().decode('utf-8')
    data[d][0] = da
    url = "https://live.aicai.com/static/no_cache/jc/zcnew/data/hist/" + \
        str(date.strftime("%y%m%d")) + "zcRefer.js"
    try:
        da = r.urlopen(url).read().decode('utf-8')
    except HTTPError:
        da = "404"
    data[d][1] = da
    print("Finish " + str(date.strftime("%Y-%m-%d")))


dt1 = pd.date_range(start="2013-01-30", end="2020-05-10", freq="D")
data = {}
for date in dt1:
    get_data(date)

json_str = json.dumps(data, ensure_ascii=False)
filename = 'scrape_data.json'
with open(filename, 'w') as fd:
    data = fd.write(json_str)
