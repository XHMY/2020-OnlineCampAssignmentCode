#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:06:17 2020

@author: yokey
"""
week_list = ["一","二","三","四","五","六","日"]
t_list = [33,45,32,56,23,56,-12]
avg = 0
print("本周每天温度:")
for i in range(0,6):
    print("星期" + week_list[i] + ": " + str(t_list[i]) + " 摄氏度")
    avg+=t_list[i]
print("\n本周平均温度: " + str(avg/7) + " 摄氏度")