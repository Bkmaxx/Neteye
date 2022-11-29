#scann
import threading
import re
import sys
import socket
from socket import *
from prettytable import PrettyTable
import dns.resolver
l=[]
table=PrettyTable(['Ports','State','Service Name'])
def Pscann(Ip,Sp,Ep):
       try:
        if __name__ == '__main__':
           target=Ip
           t_IP = gethostbyname(target)
           for i in range(Sp,Ep):
              s = socket(AF_INET, SOCK_STREAM)
              conn = s.connect_ex((t_IP, i))
              if(conn == 0) :
                 l.append(i)
                 try:               
                    service=getservbyport(i,'tcp')
                 except:
                    service='Unknown Service Running'
                 table.add_row([i,'Open',service])
                  
       except :
        pass

def Prun(Ip):
   try: 
    t_IP = gethostbyname(Ip)
    print ('Scan Report For', t_IP)   
    s=0
    for x in range(1250):
        #print('Thread t '+str(x)+' Started')                 
        tx = threading.Thread(target=Pscann, args=(Ip,s,s+50,))
        s+=50
        tx.start()
        tx.join()
    print(table)
   except KeyboardInterrupt:
    pass
     
def Pscn(Ip):
    
        startTime = str(datetime.now())
        print('Port Scan Started At : ',startTime)
        Prun(Ip)
        print('Scan Ended At ', str(datetime.now()))
    
