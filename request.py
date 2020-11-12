import os
import datetime 
from response import *
from filepermission import *
from log import *

def getReqType(text,config):
    reqType=(text.split())[0]
    try:
        if ( reqType=='GET'):
            return httpGet(text,config)
        elif ( reqType=='POST'):
            return httpPost(text,config)
        elif ( reqType=='PUT'):
            return httpPut(text,config)
        elif ( reqType=='HEAD'):
            return httpHead(text,config)
        elif ( reqType=='DELETE'):
            return httpDelete(text,config)
        else:
            return errReq(reqType, text,config,'405')
    except:
        return errReq(reqType, text,config,'403')


class httpRequest(object):
    def __init__(self, method, text, config):
        self._request=""
        self._method=method
        self._reqURI=""
        self._ver=""
        self._headers={}
        self._config=config
        self._dirpath = self._config._documentRoot

    #def setValues(self,text,config):#assigning values
        self._request=text
        self._reqURI=(text.split())[1]
        if self._reqURI == '/':
            self._reqURI = "/index.html"
        if self._method!='':
            if os.path.exists(self._dirpath+self._reqURI):
                if not check_perm(self._dirpath+self._reqURI,"r"):
                    writeLog("Error reading Requested HTML File",0,log_error)
                    raise Exception("Error reading Requested HTML File")

        self._ver=(text.split())[2]

    #def processReq(self):#splitting request into headers and body
        lines=(self._request.split('\r\n\r\n',1))
        header=(lines[0].split('\r\n'))[1:]
        self.getHeaders(header)
        self._body=lines[1:]

    def getHeaders(self,header):#sets every header and its value
        for head in header:
            l = head.split(':')
            self._headers[l[0]] = ':'.join(l[1:])

    def validateHeaders(self):
        try:
            if self._headers["Host"]!=None: #check for host header
                return True
        except:
            pass
        return False

class httpGet(httpRequest):
    def __init__(self, text, config):
        super().__init__('GET', text, config)

    def getResp(self):
        response=''
        self._reqURI = self._dirpath + self._reqURI

        if super().validateHeaders()==True:
            if os.path.exists(self._reqURI):
                response += "HTTP/1.1 200 OK\n"
                response += genHeader()
                response += respHeader(self._headers)
                response += enHeader(self._reqURI)
                response += body(self._reqURI)
            else:
                self._reqURI = self._dirpath + "/notfound.html"
                response = errResp(self._reqURI,1,"404 Page Not Found")

        else :
            self._reqURI = self._dirpath + "/error.html"
            response = errResp(self._reqURI,1,"400 Bad Request")

        return response
            

class httpPost(httpRequest):
    def __init__(self, text, config):
        super().__init__('POST', text, config) 
        vals = self._reqURI.split('?')
        self._reqURI=vals[0]
        if self._reqURI == '/':
            self._reqURI = "/index.html"
        self._data = []
        
        if (len(vals)>1):
            self._data = vals[1].split('&')
        if len(self._body)>0 and self._body[0]!="":
            temp=self._body[0].split('&')
            for val in temp:
                self._data.append(val)

    def getResp(self):
        response = ''
        self._reqURI = self._dirpath + self._reqURI

        if super().validateHeaders()==True:
            if os.path.exists(self._reqURI):
                response += "HTTP/1.1 200 OK\n"
                response += genHeader()
                response += respHeader(self._headers)
                response += enHeader(self._reqURI)
                response += body(self._reqURI)

                msg = "\nPost data recieved: "
                for key in self._data:
                    msg += str(key)
                writeLog(msg,0,log_debug)
            else : 
                self._reqURI = self._dirpath + "/notfound.html"
                response = errResp(self._reqURI,1,"404 Page Not Found")

        else :
            self._reqURI = self._dirpath + "/error.html"
            response = errResp(self._reqURI,1,"400 Bad Request")

        return response
        
    
class httpPut(httpRequest):
    def __init__(self, text, config):
        super().__init__('PUT', text, config) 

    def getResp(self):
        response=''
        self._reqURI = self._dirpath + self._reqURI

        
        if super().validateHeaders()==True:
            if self.valContentHead()==True:
                try:
                    if os.path.exists(self._reqURI):
                        open(self._reqURI,'w').close()
                        
                    file=open(self._reqURI,'a+')
                    file.write(self._body[0])
                    file.close()

                    response += "HTTP/1.1 202 Accepted\n"
                    response += genHeader()
                    response += respHeader(self._headers)
                    response += enHeader(self._reqURI)
                    #response += body(self._reqURI)
                except:
                    self._reqURI = self._dirpath + "/forbidden.html"
                    response = errResp(self._reqURI,0,"403 Forbidden")
            else:
                self._reqURI = self._dirpath + "/error.html"
                response = errResp(self._reqURI,0,"501 Not Implemented")

        else :
            self._reqURI = self._dirpath + "/error.html"
            response = errResp(self._reqURI,1,"400 Bad Request")

        return response

    def valContentHead(self):
        try:
            if self._headers["Content-Type"]!=None: #check for host header
                return True
        except:
            pass
        return False

class httpHead(httpRequest):
    def __init__(self, text, config):
        super().__init__('HEAD', text, config)

    def getResp(self):
        response=''
        self._reqURI = self._dirpath + self._reqURI

        if super().validateHeaders()==True:
            if os.path.exists(self._reqURI):
                response += "HTTP/1.1 200 OK\n"
                response += genHeader()
                response += respHeader(self._headers)
                response += enHeader(self._reqURI)
            else:
                self._reqURI = self._dirpath + "/notfound.html"
                response = errResp(self._reqURI,0,"404 Page Not Found")

        else :
            self._reqURI = self._dirpath + "/error.html"
            response = errResp(self._reqURI,0,"400 Bad Request")

        return response

class httpDelete(httpRequest):
    def __init__(self, text, config):
        super().__init__('DELETE', text, config) 

    def getResp(self):
        response=''
        self._reqURI = self._dirpath + self._reqURI

        if super().validateHeaders()==True:
            if os.path.exists(self._reqURI):
                response += "HTTP/1.1 202 Accepted\n"
                response += genHeader()
                response += respHeader(self._headers)
                response += enHeader(self._reqURI)
                try:
                    os.remove(self._reqURI)
                except:
                    self._reqURI = self._dirpath + "/notfound.html"
                    response = errResp(self._reqURI,1,"404 Page Not Found")
                #response += body(self._reqURI)
            else:
                self._reqURI = self._dirpath + "/notfound.html"
                response = errResp(self._reqURI,1,"404 Page Not Found")

        else :
            self._reqURI = self._dirpath + "/error.html"
            response = errResp(self._reqURI,1,"400 Bad Request")

        return response
    

class errReq( httpRequest):
    def __init__(self, method, text, config, errcode):
        super().__init__('', text, config) 
        self._errcode=errcode
        self._requestmethod = method

    def getResp(self):
        response=''
        needBody=1
        if self._requestmethod == 'PUT' and self._requestmethod == 'HEAD':
            needBody=0
        if self._errcode=='405':
            self._reqURI = self._dirpath + "/unsupported.html"
            response = errResp(self._reqURI,needBody,"405 Method Not Supported")
        elif self._errcode=='403':
            self._reqURI = self._dirpath + "/forbidden.html"
            response = errResp(self._reqURI,needBody,"403 Forbidden")


        return response