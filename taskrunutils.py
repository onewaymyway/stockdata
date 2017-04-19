# -*- coding: utf-8 -*-
import subprocess   
import time
import json

def isAllDone(subs):
    for p in subs:
        if p.poll() is None:
            return False
    return True

def waitAllDone(subs):
    while not isAllDone(subs):
        time.sleep(10)
        print("waiting")

def openExes(exeList,waitTime=5):
    rst=[]
    for texe in exeList:
        time.sleep(waitTime)
        print(texe)
        rst.append(subprocess.Popen(texe))
    return rst
        
def excuteExesAndWaitToEnd(exeList,waitTime=5):
    subs=openExes(exeList,waitTime)
    waitAllDone(subs)   
    
def updateWork():  
    excuteExesAndWaitToEnd(["python stockdatawork.py getdata","python stockdatawork.py getdataR"])
    excuteExesAndWaitToEnd(["D:/me/python/stocksite.git/trunk/StockCmd/bin/h5/runwithparamfull.bat"],5)

def readFile(file):
    f=open(file,"r")
    data=f.read()
    f.close()
    return data

def readJsonFile(file):
    return json.loads(readFile(file))
    
def runTaskFile(file):
    jsonO=readJsonFile(file);
    print(jsonO)
    tasks=jsonO["tasks"]
    for task in tasks:
        excuteExesAndWaitToEnd(task)
       
#excuteExesAndWaitToEnd(["D:/me/tools/ApacheSubversion/bin/svn.exe cleanup  D:/me/python/stockdata.git/trunk/stockdatas"])

#excuteExesAndWaitToEnd(["D:/me/tools/ApacheSubversion/bin/svn.exe commit -m hihi D:/me/python/stockdata.git/trunk/stockdatas"])

if __name__ == '__main__':
    runTaskFile("updateAndMakeConfigTask.json")