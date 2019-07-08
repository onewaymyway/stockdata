import subprocess
 


def updateFiles(files):
    print("files:",files)
    filesStr=" ".join(files)
    print(filesStr)
    cmds=["svn","update",filesStr]
    print(cmds)
    cmsStr=" ".join(cmds)
    print("cmsStr",cmsStr)
    #executeSvnCmd("svn cleanup")
    datas=executeSvnCmd(cmsStr)
    print("update",datas)
    
def txt_wrap_by(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()
def dealErr(errMsg):
    print(errMsg)
    errfile=txt_wrap_by("'","'",errMsg)
    errfile=errfile.replace("D:\\me\\python\\stockdata.git\\trunk\\","")
    print("errFile:",errfile)
    updateFiles([errfile])

def solveConflictFiles(files):
    print("files:",files)
    filesStr=" ".join(files)
    print(filesStr)
    #svn resolve --accept=working bar.c
    cmds=["svn","resolve --accept=working",filesStr]
    print(cmds)
    cmsStr=" ".join(cmds)
    print("cmsStr",cmsStr)
    #executeSvnCmd("svn cleanup")
    datas=executeSvnCmd(cmsStr)
    print("solveConflictFiles",datas)
    submitFiles(files)
    
def dealConflict(errMsg):
    print(errMsg)
    errfile=txt_wrap_by("'","'",errMsg)
    errfile=errfile.replace("D:\\me\\python\\stockdata.git\\trunk\\","")
    print("conflictFile:",errfile)
    solveConflictFiles([errfile])
    
def executeSvnCmd(cmds):
    p = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    datas=p.stdout.read().decode("utf-8")
    errs=p.stderr.read().decode("utf-8")
    print("myerrs:",errs)
    if errs.find("is out of date")>0:
        dealErr(errs)
    if errs.find("Conflict discovered")>0 or errs.find("remains in conflict")>0:
        dealConflict(errs)
    return datas

def getChangedFiles():
    
    datas=executeSvnCmd(['svn', 'status'])
    dlist=datas.split("\r\n")
    files=[]
    for tt in dlist:
        #print(tt)
        tfile=tt.split("       ")
        if len(tfile)<2:
            print(tt)
            continue
        if tfile[0]=="C":
            print("? conflict")
            solveConflictFiles([tfile[1].replace("\\","/")])
            continue
        if tfile[0]=="?":
            print("? add")
            submitAddFile(tfile[1].replace("\\","/"))
            continue
        tfile=tfile[1]
        tfile=tfile.replace("\\","/")
        files.append(tfile)
    
    #print(files)
    return files
    
def submitFiles(files):
    print("files:",files)
    filesStr=" ".join(files)
    print(filesStr)
    cmds=["svn","commit","-m","hihi",filesStr]
    print(cmds)
    cmsStr=" ".join(cmds)
    print("cmsStr",cmsStr)
    executeSvnCmd("svn cleanup")
    datas=executeSvnCmd(cmsStr)
    print("submit",datas)

def submitAddFile(file):
    if file.find(".csv.r")>0 or file.find(".csv.m")>0:
        return
    executeSvnCmd("svn add "+file)
    executeSvnCmd("svn commit -m hihi "+file)
    
def workLoop():
    changefiles=getChangedFiles()
    allLen=len(changefiles)
    print(allLen)
    sublen=allLen
    maxLen=50
    if sublen>maxLen:
        sublen=maxLen
    if sublen<1:
        return False

    submitFiles(changefiles[0:maxLen])
    return sublen>=maxLen
    
def doWork():
    while True:
        rst=workLoop()
        if rst:
            pass
        else:
            break
#datas=executeSvnCmd('svn commit -m hihi stockdatas/000009.csv stockdatas/000010.csv')
#print(datas)
#workLoop()
doWork()