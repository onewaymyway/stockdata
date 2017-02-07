import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
import datetime
import time
import os
import pandas as pd
import sys
from multiprocessing.dummy import Pool as ThreadPool

stockBasicInfo=None
myG={}
workingStock=[]

def getStockInfo(stock):  
    data=ts.get_hist_data(stock)
    print(data)

def initStockBasic():
    global stockBasicInfo,myG
    stockBasicInfo=ts.get_stock_basics()
    #print(stockBasicInfo)
    codes=stockBasicInfo.index
    print(codes)
    myG["codes"]=codes
    stockBasicInfo.to_csv("stockinfo.csv",encoding="utf8")

    
def getStockBeginDay(stock):
    global stockBasicInfo
    df = stockBasicInfo
    date = df.ix[stock]['timeToMarket'] #上市日期YYYYMMDD
    #print(df.ix[stock])
    #print(date)
    
    timeArray = time.strptime(str(date),'%Y%m%d')
    newdate=time.strftime("%Y-%m-%d",timeArray)
    return newdate

def isStockOnMarket(stock):
    global stockBasicInfo
    df = stockBasicInfo
    date = df.ix[stock]['timeToMarket'] #上市日期YYYYMMDD
    #print(df.ix[stock])
    if date==0:
        return False
    return True

def getStockData(stock,start,end):
    filepath="stockdatas/"+stock+".csv"
    if os.path.exists(filepath):
        print("getDataFromDisk:",stock)
        hist_data=pd.read_csv(filepath,index_col="date")
    else:  
        print("getDataFromNet:",stock,start,end)
        hist_data=ts.get_h_data(stock,start,end)
        print("saveData:",stock)
        print(type(hist_data))
        if type(hist_data)==type(None):
            return None
            
        hist_data.to_csv(filepath)
    return hist_data
    
#getStockInfo("600848")

def saveStockKLine(stock,start,end):
    filepath="stocks/"+stock+".png"
    if os.path.exists(filepath):
        return
    
    hist_data=getStockData(stock,start,end)
    if type(hist_data)==type(None):
        return;
    print("transData:",stock)
    # 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
    data_list = []
    #print(hist_data)
    if not hist_data.iterrows():
        return;
    
    for dates,row in hist_data.iterrows():
        # 将时间转换为数字
        #print(dates)
        #print(type(dates)==str)
        if type(dates)==str:
            date_time = datetime.datetime.strptime(dates,'%Y-%m-%d')
        else:     
            date_time=dates
        t = date2num(date_time)
        #open,high,low,close = row[:4]
        open,high,close,low = row[:4]
        datas = (t,open,high,low,close)
        data_list.append(datas)

    print("drawData:",stock)
    # 创建子图
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    # 设置X轴刻度为日期时间
    ax.xaxis_date()
    plt.xticks(rotation=45)
    plt.yticks()
    plt.title("Code："+stock+"")
    plt.xlabel("Time")
    plt.ylabel("Price")
    mpf.candlestick_ohlc(ax,data_list,width=1,colorup='r',colordown='green')
    plt.grid()
    fig.savefig(filepath)
    plt.close("all")
    print("savedPic:",stock)


def getToday():
    now=datetime.datetime.now()
    nowstr=now.strftime("%Y-%m-%d")
    return nowstr

def workAStock(stock):
    start=getStockBeginDay(stock)
    end=getToday()
    saveStockKLine(stock,start,end);

def workStocks(stocks):
    for stock in stocks:
        if isStockOnMarket(stock)==False:
            continue;
        workAStock(stock)

def updateStockDataWork(stock):
    start=getStockBeginDay(stock)
    end=getToday()
    getStockData(stock,start,end);

def analyseWorkLoop():
    initStockBasic()
    #workAStock("000993")
    workStocks(myG["codes"])

def updateStocks(stocks):
    for stock in stocks:
        #print(stock)
        if isStockOnMarket(stock)==False:
            continue;
        updateStockDataWork(stock)

def updateDataWorkLoop(reverse=False):
    initStockBasic()
    print("updateDataWorkLoop")
    stocks=myG["codes"]
    stocks=list(stocks)
    #print(stocks)
    if reverse:
        stocks.reverse()
    
    updateStocks(stocks)

def threadwork(stock):
    print("work:",stock)
    if stock in workingStock:
        return
    workingStock.append(stock)
    if isStockOnMarket(stock)==False:
            return;
    updateStockDataWork(stock)
    return stock
    
def threadpoolwork(reverse=False):
    initStockBasic()
    print("updateDataWorkLoopPool")
    stocks=myG["codes"]
    stocks=list(stocks)
    #print(stocks)
    if reverse:
        stocks.reverse()
    pool=ThreadPool(20)
    print(pool)
    try:
        pool.map(threadwork,stocks)
    except:
        pool.map(threadwork,stocks)
    pool.close();
    pool.join()
    
def threadworkPic(stock):
    print("work:",stock)
    if stock in workingStock:
        return
    workingStock.append(stock)
    if isStockOnMarket(stock)==False:
            return;
    workAStock(stock)
    return stock
    
def threadpoolworkPic(reverse=False):
    initStockBasic()
    print("updateDataWorkLoopPool")
    stocks=myG["codes"]
    stocks=list(stocks)
    #print(stocks)
    if reverse:
        stocks.reverse()
    pool=ThreadPool(4)
    print(pool)
    try:
        pool.map(threadworkPic,stocks)
    except:
        pool.map(threadworkPic,stocks)
    pool.close();
    pool.join()    

if __name__=="__main__" :
    
    print(sys.argv)
    if len(sys.argv)==2:
        workType=sys.argv[1]
        print(workType)
        if workType=="getdata":
            updateDataWorkLoop()
        if workType=="getdataR":
            updateDataWorkLoop(True)
        if workType=="threadGetData":
            threadpoolwork()
        if workType=="getbasicInfo":
            initStockBasic()
    else:
        #analyseWorkLoop()
        threadpoolworkPic()
        #updateDataWorkLoop(True)
        #threadpoolwork()
    print("done")

