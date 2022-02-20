import time

def dateFormatted(format = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime())