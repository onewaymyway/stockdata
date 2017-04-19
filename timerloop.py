# -*- coding: utf-8 -*-

import time
import datetime

dayTimeS=24*60*60;

def getTimeStamp(timeStr):
    timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S");
    timeStamp = int(time.mktime(timeArray));
    return timeStamp;
    
def getTimeStr():
    now=datetime.datetime.now();
    dayTime=now.strftime("%Y-%m-%d");
    print(dayTime);
    return dayTime;

def getTimeStrN():
    now=datetime.datetime.now();
    dayTime=now.strftime("%Y-%m-%d  %H:%M:%S");
    return dayTime;

def getNow():
    return int(time.time());

class TimeList:

    def __init__(self,fileName="timeList.txt"):
        global dayTimeS;
        self.TID=1
        times={};
        self.times=times;
        

    def getNextTime(self,timeStr):
        daytime=getTimeStr();
        nextTime=getTimeStamp(daytime+" "+timeStr);
        if nextTime<getNow():
            nextTime=nextTime+dayTimeS;
        return nextTime

    def addTask(self,timeStr,fun,msg):
        tTimeO={}
        tTimeO["time"]=timeStr
        tTimeO["fun"]=fun
        tTimeO["msg"]=msg
        tTimeO["ctime"]=self.getNextTime(timeStr)
        self.TID=1+self.TID
        self.times[self.TID]=tTimeO

    def tick(self):
        global dayTimeS;
        tTime=int(time.time());
        print("tTime:"+getTimeStrN());
        
        for timest in self.times:
            cTime=self.times[timest];
            if int(cTime["ctime"])<=tTime:
                #print("time:"+cTime["msg"]);
                cTime["ctime"]=int(cTime["ctime"])+dayTimeS;
                print("next:"+str(cTime["ctime"]));
                print("msg:",cTime["msg"])
                if cTime["fun"]:
                    cTime["fun"]();

    def beginRun(self,okTime=10,exceptionTime=5):
        while(1):
            try:
                self.tick();
                time.sleep(okTime)
            except Exception as e:
                print(e)
                time.sleep(exceptionTime)
      
def mainLoop():
    tT=TimeList();
    tT.addTask("15:09:50",None,"hihi")
    tT.addTask("15:10:50",None,"hihiee")
    tT.beginRun()



if __name__ == '__main__':
    mainLoop()