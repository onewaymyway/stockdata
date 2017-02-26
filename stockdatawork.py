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
blackList=["000033"]

def getStockInfo(stock):  
    data=ts.get_hist_data(stock)
    print(data)

def getOKStockCode(code):
    code=str(code)
    for i in range(0,6):
        if len(code)<6:
            code="0"+code
    return code
    
def initStockBasic():
    global stockBasicInfo,myG

    
    if 1<0:
        myG["basicfromcsv"]=True;
        stockBasicInfo=pd.read_csv("stockinfo.csv",index_col="code")
    else:
        myG["basicfromcsv"]=False;
        stockBasicInfo=ts.get_stock_basics()


    #print(stockBasicInfo)
    codes=list(stockBasicInfo.index)
    for i in range(0,len(codes)):
        codes[i]=getOKStockCode(codes[i])
    print(codes)
    myG["codes"]=codes
    for tstock in blackList:
        print(tstock)
        codes.remove(tstock)
        
    stockBasicInfo.to_csv("stockinfo.csv",encoding="utf8")

    
def getStockBeginDay(stock):
    global stockBasicInfo
    df = stockBasicInfo
    #print(df)
    if myG["basicfromcsv"]==True:
        stock =int(stock)
    #print(stock)
    date = df.ix[stock]['timeToMarket'] #上市日期YYYYMMDD
    #print(df.ix[stock])
    #print(date)
    
    timeArray = time.strptime(str(date),'%Y%m%d')
    newdate=time.strftime("%Y-%m-%d",timeArray)
    return newdate

def isStockOnMarket(stock):
    global stockBasicInfo
    df = stockBasicInfo
    #print(df)
    if myG["basicfromcsv"]==True:
        stock =int(stock)
    date = df.ix[stock]['timeToMarket'] #上市日期YYYYMMDD
    
    if date==0:
        return False
    return True

def getStockData2(stock,start,end):
    filepath="stockdatas/"+stock+".csv"
    if os.path.exists(filepath):
        print("getDataFromDisk:",stock)
        hist_data=pd.read_csv(filepath,index_col="date")
        hindex=hist_data.index
        print(max(hindex))
        premax=max(hindex)
        #print(hist_data.ix[premax])
        #print(hist_data)
        hist_data=hist_data.drop(premax)
        #print(hist_data)
        #return
        if premax==getToday():
            return hist_data

        newdata=ts.get_h_data(stock,premax,getToday())
        newdata.to_csv(filepath)
        newdata=pd.read_csv(filepath,index_col="date")
        print(newdata)
     
        tdata=pd.concat([newdata,hist_data])

        #print(tdata)
        tdata.to_csv(filepath)
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
    
def getStockData(stock,start,end):
    #return getStockData2(stock,start,end)
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
    print("candlestick_ohlc")
    mpf.candlestick_ohlc(ax,data_list,width=1,colorup='r',colordown='green')
    print("grid");
    plt.grid()
    print("savefig");
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

def updateStockDataWork(stock,updating=False):
    start=getStockBeginDay(stock)
    end=getToday()
    if updating==False:
        getStockData(stock,start,end);
    else:
        getStockData2(stock,start,end);
    #getStockData(stock,start,end);

def analyseWorkLoop(reverse=False):
    initStockBasic()
    #workAStock("000993")
    stocks=myG["codes"]
    stocks=list(stocks)
    #print(stocks)
    if reverse:
        stocks.reverse()
    workStocks(stocks)

def updateStocks(stocks):
    for stock in stocks:
        #print(stock)
        if isStockOnMarket(stock)==False:
            continue;
        try:
            updateStockDataWork(stock,True)
        except:
            pass
        

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
    updateStockDataWork(stock,True)
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
        if workType=="getpicR":
            analyseWorkLoop(True)
    else:
        analyseWorkLoop()
        #threadpoolworkPic()
        #updateDataWorkLoop(True)
        #threadpoolwork()
        #initStockBasic()
        #updateStockDataWork("600641")
    print("done")

