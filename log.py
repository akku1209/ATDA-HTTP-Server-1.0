
from datetime import *
import os
from config import *
from filepermission import *

log_debug='DEBUG: ' 
log_warn='WARNING: '
log_error='ERROR: '

filename=''

def setLogConfig(config):
    global filename
    dirpath=('/'.join((__file__.split('/'))[:-1]))+"/Log"
    if config._logFileName!='':
        try:
            os.mkdir(dirpath) 
        except:
            pass
        if not check_perm(dirpath,"w"):
            print("Error creating Log File")
            return
        filename = dirpath+'/'+config._logFileName
        #self._file = open(filename, "a+")

def writeLog(text,ifPrint,level):
    if(filename!=''):
        file = open(filename, "a+")
        if not check_perm(filename,"w"):
            print (filename)
            print("Error writting in Log File")
            return
        file.write(level+str(datetime.now())+" :"+text+"\n")
        file.close()

    if(ifPrint==1):
        print(text)



    