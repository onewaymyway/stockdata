import os
import hashlib
import json
import shutil
mdData={}
configO={}
gPath=""
workPath="E:/wangwei/serviceworker/testserviceworker/trunk/layaserviceworker/bin/h5"
cacheSign="LayaAirGameCache";
workerPath="service-worker.js";
excludeFileDic={}

def formatPath(path):
    path=path.replace(gPath,"")
    path=path.replace("\\","/")
    return path;
def getWorkPath(relativePath):
    return os.path.join(workPath,relativePath);

def getFileMd5(path):
    fp = open(path,"rb") #open file. There is a big problem here. That is when you get a large file.
    c = fp.read() # get file content.
    m = hashlib.md5() # create a md5 object
    m.update(c) #encrypt the file
    fp.close() #close file
    return str(m.hexdigest())

def isWorkFile(path):
    path=formatPath(path)
    if path in excludeFileDic:
        return False
    return True

def walk(path):
    fl = os.listdir(path) # get what we have in the dir.
    for f in fl:
        tFilePath=os.path.join(path,f);
        if not isWorkFile(tFilePath):
            continue;
        if os.path.isdir(os.path.join(path,f)): # if is a dir.      
            walk(os.path.join(path,f))
        else: # if is a file
                    
            tPath=formatPath(tFilePath)
            mdData[tPath]=getFileMd5(os.path.join(path,f))
            

def initConfig(filePath):
    global workPath,cacheSign,workerPath,excludeFileDic
    f=open(filePath,"r");
    jsontxt=f.read();
    f.close()
    jsono=json.loads(jsontxt)
    print(jsono)
    workPath=jsono["workDir"]
    if "cacheSign" in jsono:
        cacheSign=jsono["cacheSign"]
    if "workerPath" in jsono:
        workerPath=jsono["workerPath"]
    excludeFileDic={};
    excludeFileDic["workerconfig.json"]=True;
    excludeFileDic["fileconfig.json"]=True;
    excludeFileDic[workerPath]=True;
    if "exclude" in jsono:
        excludeList=jsono["exclude"]
        for exfile in excludeList:
            excludeFileDic[exfile]=True
    print(excludeFileDic)

def copyWorkerJS():
    shutil.copyfile("service-worker.js",getWorkPath(workerPath));
    
def createFileVerFile():
    f=open(getWorkPath("fileconfig.json"),"w")
    f.write(json.dumps(mdData,sort_keys=True))
    f.close();
    
def createConfigFile():
    configData={};
    configData["cacheSign"]=cacheSign;
    configData["workerPath"]=workerPath;
    configData["fileVer"]=getFileMd5(getWorkPath("fileconfig.json"));
    f=open(getWorkPath("workerconfig.json"),"w")
    f.write(json.dumps(configData,sort_keys=True))
    f.close();
    
def beginWork(configPath):
    global gPath,mdData
    initConfig(configPath);
    mdData={}
    rPath=os.getcwd();
    gPath=workPath+"\\"
    print("workPath",workPath);
    walk(workPath)
    createFileVerFile();
    createConfigFile();
    copyWorkerJS();
    print(mdData)

    
if __name__ == "__main__":
    beginWork("serviceworkerconfig.json");
