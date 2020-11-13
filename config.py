import configparser
import os
from filepermission import *

keys=['DocumentRoot','LogFileName','MaxConnections']

class configuration(object):
    def __init__(self):
        self._documentRoot = ('/'.join((__file__.split('/'))[:-1]))
        self._logFileName = 'serverlog.txt'
        self._maxConnections = 10 

    def read_config(self):
        import log
        path=('/'.join((__file__.split('/'))[:-1])) + '/server.config'
        if not check_perm(path,"r"):
            log.writeLog("Error reading Config File",1,log.log_error)
            return
    
        config = configparser.ConfigParser()
        #config.sections()
        config.read(path)
        vals=[self._documentRoot ,self._logFileName ,self._maxConnections]
        for i,key in enumerate(keys):
            try:
                vals[i] = config['DEFAULT'][key]
            except:
                pass
        if vals[0]!='':
            self._documentRoot = vals[0]
        if vals[1]!='':
            self._logFileName = vals[1]
        if vals[2]!='':
            self._maxConnections = vals[2]

        #print (self._documentRoot,self._logFileName,self._maxConnections)