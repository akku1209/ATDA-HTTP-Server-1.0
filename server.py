#server side code for http webserver

from socket import *
import sys
import os
from datetime import datetime
import time as t
from log import *
from request import *
from threading import *
from response import *

server_socket=None
connections=[]

def server_thread(config,connect_socket,connections,address):
    try:
        reqstr = connect_socket.recv(2048).decode()
        writeLog(reqstr,0,log_debug)
        httpReq = getReqType(reqstr,config)

        #httpReq.setValues(reqstr,config)
        #httpReq.processReq()
        t.sleep(1) #uncomment this to check maximum connections without tester program

        response=httpReq.getResp()
        writeLog(response,0,log_debug)
        connect_socket.send(response.encode())
    except:
        writeLog("Fatal Error while Processing!",1,log_error) 
        pass
    writeLog("Connection with IP: "+str(address[0])+" has been closed",1,log_debug)
    try: 
        connect_socket.close()
    except:
        pass
    connections.remove(connect_socket) 

def startServer(config):
    host = '127.0.0.1'
    global server_socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    #server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    port = int(sys.argv[1])
    server_socket.bind(('', port))
    server_socket.listen(100)
    writeLog("Server is up and listening...",1,log_debug)

    try:
        while True:
            if len(connections)>=int(config._maxConnections):
                writeLog("Maximum Connections Reached.",1,log_warn)
                t.sleep(1)
                continue
            connect_socket, address = server_socket.accept()
            connections.append(connect_socket)
            writeLog("New Request Recieved from IP: "+str(address[0])+" and Port: "+str(port),1,log_debug)
            thread = Thread(target=server_thread, args=(config,connect_socket,connections,address))
            thread.start()

    except IOError:
        err_type, value, traceback = sys.exc_info()
        #print('Error opening %s: %s' % (value.filename, value.strerror)):
        writeLog("Fatal Error in Connection! Exception Type: "+err_type+" and Value: "+value,1,log_error) 

def stopServer(errcode):
    global server_socket
    server_socket.close()
    if(errcode!=0):
        print('Fatal Error!')
        