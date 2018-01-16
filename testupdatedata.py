# -*- coding: utf-8 -*-
import tushare as ts

kData=ts.get_k_data("601918","2017-09-01","2017-09-06")
print(kData)
kData=ts.get_h_data("601918","2017-09-01","2017-09-06")
print(kData)
todayData=ts.get_today_all()
todayO=todayData[todayData.code=="601918"];
print("get_today_all",todayO)
print(todayO["volume"])
todayData=ts.get_day_all("2017-09-07")
todayO=todayData[todayData.code=="601918"];
print("get_day_all",todayO)
print(todayO["volume"])