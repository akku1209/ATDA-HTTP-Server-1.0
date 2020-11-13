from threading import *
from server import *
from config import *

config=configuration()
config.read_config()
setLogConfig(config)

try:
    port = int(sys.argv[1])
except:
    print("Invalid parameters.\nProvide Port number.")
    os._exit(1)

silent_run=0
if len(sys.argv)>2:
    if sys.argv[2] =='--start':  
        silent_run=1

#'start' to start the server; 'pause' to temporarily pause the server; 'stop' to end the program
def checkInput(inp):
    #while True:
    if inp.upper()=="START" or inp.upper()=="1": 
        print("--> ATDA HTTP Server is starting!")
        startServer(config)
        
    elif inp.upper()=="PAUSE" or inp.upper()=="2": 
        try:
            pauseServer(0)
            print("--> ATDA HTTP Server is pausing! Input Start for continuing execution and Stop to end program.")
        except:
            print("Can't pause server without starting it.")
            return
        
    elif inp.upper()=="STOP" or inp.upper()=="3":
        try:
            stopServer(0)
        except:
            pass
        print("--> ATDA HTTP Server has stopped! \n-->Thank You for using ATDA Server.")        
        os._exit(1)

print("-->Menu: \n1. Start -> To start the server \n2. Pause -> To temporarily pause the server \n3. Stop -> To stop the server and end the program")
while True:
    if silent_run==0:
        inp=input()
    else:
        inp="1"
        silent_run=0
    t = Thread(target=checkInput, args=(inp,))
    t.start()
