#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:34:59 2020

@author: yokey
"""

from functools import reduce

weat_dict = {
    '一': ["晴",23.3],
    '二': ["雨",12.3],
    '三': ["云",83.3],
    '四': ["雾",543.3],
    '五': ["沙尘暴",223.3],
    '六': ["龙卷风",2123.32],
    '日': ["海啸",-9323.3]
    }

## max_temp = -99999999.99;

def find_max(a, b):
    if a < b:
        return b
    else:
        return a
temp_list = []
for key in weat_dict:
    print("星期" + key + "的天气是"+ weat_dict[key][0] 
          + ", 温度是" + str(weat_dict[key][1]) + "摄氏度")
    temp_list.append(weat_dict[key][1])
##    if(max_temp<weat_dict[key][1]):
##        max_temp = weat_dict[key][1]
    
## 用Reduce函数实现找到最大值
print("这周最高温度是" + str(reduce(find_max, temp_list)) + "摄氏度")