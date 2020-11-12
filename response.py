import os
from datetime import datetime
from log import *
import random

def genHeader():     
    #Connection 
    hdr=''  
    curr_time = datetime.now() 
    hdr += ("Date: " + curr_time.strftime("%A") + ", "+ curr_time.strftime("%d") + " " +  curr_time.strftime("%b") + " " + curr_time.strftime("%Y") + " " + curr_time.strftime("%X") + " GMT\n")           
    #Warning
    return hdr 

def respHeader(headers):
    hdr = "Server: ATDA HTTP Server/1.0.0 \n"
    hdr += "Accept-Ranges: none\n"
    try:
        t1=headers['Cookie']
        if headers["Cookie"]!=None:
            hdr += "Set-Cookie:"+headers.get("Cookie") +"\n"
    except:
        hdr += "Set-Cookie: Session-Id = "+ str(random.randint(0,99999999999999))+"\n"
    
    #Location  
    hdr += "Vary: *\n"
    return hdr

def enHeader(reqURI):
    hdr = ''
    hdr = "Allow: GET, POST, HEAD, DELETE, PUT\n"
    #Content-Encoding
    hdr += "Content-Language: en-US\n" 
    content_length = os.path.getsize(reqURI)
    hdr += "Content-Length: " + str(content_length) + "\n"
    #Content-Location
    #Expires
    last_modified = os.path.getmtime(reqURI)
    hdr += ("Last-Modified: " + datetime.fromtimestamp(last_modified).strftime("%A, %d %b, %Y %I:%M:%S")+ " GMT\n")
    hdr += "Content-Type: text/html; charset=UTF-8\n\n"
    return hdr

def body(reqURI):
    reqfile = open(reqURI, 'r')
    b=reqfile.read()
    reqfile.close()
    return b

def errResp(reqURI,body_flag,err_code):
    if not check_perm(reqURI,"r"):
        writeLog("Error reading Requested Error HTML File",1,log_error)
        return 
    requested_file = open(reqURI, 'r')
    response = "HTTP/1.1 "+err_code+"\n"
    curr_time = datetime.now()
    response += ("Date: " + curr_time.strftime("%A") + ", "+ curr_time.strftime("%d") + " " +  curr_time.strftime("%b") + " " + curr_time.strftime("%Y") + " " + curr_time.strftime("%X") + " GMT\n")
    response += "Server: ATDA/1.0.0 \n"
    content_length = os.path.getsize(reqURI)
    response += "Content-Length: " + str(content_length) + "\n"
    #if(body_flag==1):
        #response += "Connection: close\n"
    response += "Content-Type: text/html; charset=iso-8859-1\n\n"
    if body_flag==0:
        return response
    response += requested_file.read()
    requested_file.close()
    return response