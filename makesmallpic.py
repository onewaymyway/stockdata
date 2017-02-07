from PIL import Image
import os
import hashlib
import json
import shutil

size=100,75
def makeSmallPic(picpath):
    print("makeSmallPic:",picpath)
    im=Image.open(picpath)
    im.thumbnail(size,Image.ANTIALIAS)
    im.save(picpath.replace("stocks","smallpics"),"JPEG")

#makeSmallPic("stocks/000001.png")
def isWorkFile(path):
    if path.find(".png"):
        return True
    return False
def walk(path):
    fl = os.listdir(path) # get what we have in the dir.
    for f in fl:
        tFilePath=os.path.join(path,f);
        if not isWorkFile(tFilePath):
            continue;
        if os.path.isdir(os.path.join(path,f)): # if is a dir.      
            walk(os.path.join(path,f))
        else: # if is a file
                    
            makeSmallPic(tFilePath)

walk("stocks")
    