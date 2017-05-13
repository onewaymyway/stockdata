import shutil
import sys

def copyfile(old,new):
    shutil.copyfile(old,new)
    
if __name__=="__main__" :
    
    print(sys.argv)
    if len(sys.argv)==3:
        copyfile(sys.argv[1],sys.argv[2])