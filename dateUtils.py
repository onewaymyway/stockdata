import datetime


def getWeekDay():
    d=datetime.datetime.now()
    rst=d.weekday()
    return rst

def isWorkDay():
    td=getWeekDay()
    return td<5