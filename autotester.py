import random
import os
import datetime
import pexpect
#import httplib2
import requests
from threading import *
import configparser
from requests.exceptions import ConnectionError
import os
import sys
import time as t
import subprocess

port =random.randint(1024,9999) #generating random port number
path = ('/'.join((__file__.split('/'))[:-1])) + "/Report/"
if os.path.isdir(path) :
    pass
else:
    os.mkdir(path)


cmdLine = '/'.join((__file__.split('/'))[:-1])+'/main.py'
print(cmdLine)
process = subprocess.Popen(
    ['python3', cmdLine, str(port), '--start'], stdin=subprocess.PIPE, stdout=subprocess.PIPE
)
t.sleep(3)
#process.stdin.write(b'1')

#t.sleep(2)

def report(rfile,text,ifprint):
    rfile.write(text)
    if ifprint==1:
        print(text)
    

maxConn=0
def read_config():
    global maxConn
    path=('/'.join((__file__.split('/'))[:-1])) + '/server.config'

    config = configparser.ConfigParser()
    #config.sections()
    config.read(path)
    try:
        if config._defaults['maxconnections']!='':
            maxConn=int(config._defaults['maxconnections'])
    except:
        maxConn = 3



p_count=0
f_count=0
mutex = Lock()
def inc_count(method,rfile,val,exp):
    mutex.acquire()
    global p_count,f_count
    if(val==exp):
        p_count+=1
    else:
        f_count+=1
        #print(method+" Failed")
    report( rfile,'Expected status code: '+str(exp),1)
    report( rfile,'    Actual status code: '+str(val),1)
    mutex.release()

def http_server_test():
    filename = path + "report_"+ str(datetime.datetime.now())
    rfile = open(filename,"w+")
    report( rfile,'Port Number is '+str(port),1)

    try:
        ###GET=========================================================
        #200 get request
        url='http://127.0.0.1:'+str(port)+'/'
        r = requests.get(url)
        report( rfile,'\n\n-->Running test for GET',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('GET',rfile,r.status_code,200)

        #page not found get request
        url='http://127.0.0.1:'+str(port)+'/blabla.html'
        r = requests.get(url)
        report( rfile,'\n\n-->Running test for GET ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('GET',rfile,r.status_code,404)

        #forbidden get
        url='http://127.0.0.1:'+str(port)+'/priv.html'
        r = requests.get(url)
        report( rfile,'\n\n-->Running test for GET ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('GET',rfile,r.status_code,403)

        ###POST===========================================================
        #good post request
        vals = {'fname': '123'  , 'lname': '456'}
        url='http://127.0.0.1:'+str(port)+'/postform.html'
        r = requests.post(url,data=vals)
        report( rfile,'\n\n-->Running test for POST ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('POST',rfile,r.status_code,200)

        #page not found post request
        vals = {'fname': '123'  , 'lname': '456'}
        url='http://127.0.0.1:'+str(port)+'/blabla.html'
        r = requests.post(url,data=vals)
        report( rfile,'\n\n-->Running test for POST ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('GET',rfile,r.status_code,404)

        #forbidden post
        vals = {'fname': '123'  , 'lname': '456'}
        url='http://127.0.0.1:'+str(port)+'/priv.html'
        r = requests.post(url,data=vals)
        report( rfile,'\n\n-->Running test for POST ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('GET',rfile,r.status_code,403)

        ###PUT============================================================
        #good put request

        #page not existing request
        headers = {'Content-Type': 'text/plain'}
        url='http://127.0.0.1:'+str(port)+'/temps/temp_'+str(random.randint(0,100))+'.html'
        d_url=url
        try:
            r = requests.put(url, data ="Temporary file for PUT "+str(random.randint(0,100)), headers=headers) 
        except:
            pass
        report( rfile,'\n\n-->Running test for PUT ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('PUT',rfile,r.status_code,202)

        #folder/page not existing request
        headers = {'Content-Type': 'text/plain'}
        url='http://127.0.0.1:'+str(port)+'/abc/blabla232.html'
        try:
            r = requests.put(url, data ="Temporary file for PUT "+str(random.randint(0,100)), headers=headers) 
        except:
            pass
        report( rfile,'\n\n-->Running test for PUT ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('PUT',rfile,r.status_code,403)

        #fcontent header
        url='http://127.0.0.1:'+str(port)+'/temps/blabla_'+str(random.randint(0,100))+'.html'
        r = requests.put(url, data ="Temporary file for PUT "+str(random.randint(0,100))) 
        report( rfile,'\n\n-->Running test for PUT ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('PUT',rfile,r.status_code,501)

        #file permission
        headers = {'Content-Type': 'text/plain'}
        url='http://127.0.0.1:'+str(port)+'/priv.html'
        r = requests.put(url, data ="Temporary file for PUT "+str(random.randint(0,100)), headers=headers) 
        report( rfile,'\n\n-->Running test for PUT ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('PUT',rfile,r.status_code,403)


        ###HEAD=============================================================
        #200 head request
        url='http://127.0.0.1:'+str(port)+'/'
        r = requests.head(url)
        report( rfile,'\n\n-->Running test for HEAD ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('HEAD',rfile,r.status_code,200)

        #page not found head request
        url='http://127.0.0.1:'+str(port)+'/blabla.html'
        r = requests.head(url)
        report( rfile,'\n\n-->Running test for HEAD ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('HEAD',rfile,r.status_code,404)

        #forbidden head
        url='http://127.0.0.1:'+str(port)+'/priv.html'
        r = requests.head(url)
        report( rfile,'\n\n-->Running test for HEAD ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('HEAD',rfile,r.status_code,403)

        ###DELETE=========================================================
        #good delete request
        url=d_url
        r = requests.delete(url)
        report( rfile,'\n\n-->Running test for DELETE ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('DELETE',rfile,r.status_code,202)

        #page not found request
        url='http://127.0.0.1:'+str(port)+'/87654.html'
        r = requests.delete(url)
        report( rfile,'\n\n-->Running test for DELETE ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('DELETE',rfile,r.status_code,404)

        #forbidden delete request
        url='http://127.0.0.1:'+str(port)+'/priv.html'
        r = requests.delete(url)
        report( rfile,'\n\n-->Running test for DELETE ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('DELETE',rfile,r.status_code,403)

        ###not supported method==========================================
        url='http://127.0.0.1:'+str(port)+'/index.html'
        r = requests.request('PATCH', url)
        report( rfile,'\n\n-->Running test for PATCH ',1)
        report( rfile,'\nURL: '+ url+'\nStatus Code= '+str(r.status_code),0)
        inc_count('PATCH',rfile,r.status_code,405)
    except Exception as e: 
        report( rfile,'\nConnection refused by server. Possible maximum connections reached', 1)
    #report( rfile,'\nTests passed: '+str(p_count)+'\nTests failed: '+str(f_count)+'\nTotal tests conducted: '+str(p_count+f_count),1)  

    rfile.close()


read_config()
count=0
threads=[]
while count<maxConn+5:
    threads.append(Thread(target=http_server_test, args=()))
    threads[count].start()
    count+=1

#wait till al threads stop
count=0
while count<len(threads):
    threads[count].join()
    count+=1

input("Test finished. Press Enter for Report.")
#process.sendline('3')
print('\nTests passed: '+str(p_count)+'\nTests failed: '+str(f_count)+'\nTotal tests conducted: '+str(p_count+f_count))

#print("\nTest finished")

process.stdin.write(b'3')
