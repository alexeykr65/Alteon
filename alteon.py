#!/usr/bin/env python
#
# Get configuration for Alteon
#
# alexeykr@gmail.com
#
import sys
import argparse
import string
import re
import random
import requests
import zlib
import datetime

listAlteon = ['192.168.180.61', '192.168.180.62', '192.168.180.63', '192.168.180.64', '192.168.180.75', '192.168.180.76']
altUser = "admin"
altPass = "admin"
myAuth=requests.auth.HTTPBasicAuth(altUser, altPass)

description = "alteon: Get and Set Information from Alteon"
epilog = "ciscoblog.ru"

flagDebug = int()
flagL2vpn = int()
flagReset = int()
sterraConfig = dict()

fileName = ""
keyPreShare = ""
nameInterface = ""

def getCfgAlteon():
    global flagDebug
    
    for sAlteon in listAlteon:
        if flagDebug > 1: print "Alteon Ip address: ", sAlteon
        reqUrl = "https://"+sAlteon+"/config/getcfg"            
        r = getRequests(reqUrl, 1, "")
        if(r):
            zDecompress = zlib.decompress(r.content, zlib.MAX_WBITS|32)
            year, month, day, hour, minn, sec = getDate()
            fileName = '-'.join(["Alteon", sAlteon, "config", year, month, day, hour, minn, sec + ".txt"])
            if flagDebug > 1: print " Filename cfg: "+fileName
            writeFile(zDecompress, fileName)

def rstAlteon():
    global flagDebug, flagReset
    
    if(flagReset == 0):
        for sAlteon in listAlteon:
            if flagDebug > 1: print "Alteon Ip address: ", sAlteon
            reqUrl = "https://"+sAlteon+"/config"            
            r = getRequests(reqUrl, 2, '{"agReset":"2"}')
    else:
        sAlteon = listAlteon[flagReset-1]
        if flagDebug > 1: print "Alteon Ip address: ", sAlteon
        reqUrl = "https://"+sAlteon+"/config"            
        r = getRequests(reqUrl, 2, '{"agReset":"2"}')
    
def getRequests(pReqUrl, pMethod, pParam):
    global myAuth, flagDebug    
    requests.packages.urllib3.disable_warnings()
    count = 4
    while(count > 1):
        try:
            if(pMethod == 1):
                r = requests.get(pReqUrl, auth=myAuth, verify=False, timeout=10)
            elif(pMethod == 2):
                r = requests.put(pReqUrl, auth=myAuth, verify=False, timeout=10, data=pParam)
        except requests.ConnectionError, e:
            print "Error : ", e 
            return 0
        if(r.status_code == 200):
            if flagDebug > 1: print "Status: ", r.status_code
            count = 0
        else:
            count = count - 1
            if flagDebug > 1: print "Status else: ", r.status_code
    return r
          
def cmdArgsParser():
    global fileName, keyPreShare, nameInterface, flagDebug, flagFullMesh, flagL2vpn
    if flagDebug > 0: print "Analyze options ... "
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('-f', '--file', help='File name with source data', dest="fileName", default = 'sterra.conf')
    parser.add_argument('-c', '--getcfg', help='Get Config From Alteon', action="store_true")
    parser.add_argument('-r', '--reset', help='Reset Alteons', action="store", dest="flagReset", default=0)
    parser.add_argument('-i', '--interface', help='Name of interfaces (default GigabitEthernet)', action="store",  dest="nameInterface", default="GigabitEthernet")
    parser.add_argument('-d', '--debug', help='Debug information view(default =1, 2- more verbose', dest="flagDebug", default=1)
    parser.add_argument('-m', '--mesh', help='Enable Full Mesh(default = disable', action="store_true")
    parser.add_argument('-l2', '--l2vpn', help='Generate configuration for L2 VPN', action="store_true")
    flagDebug = 2
    return parser.parse_args()

def getDate():
    #Get Date
    now = datetime.datetime.now()
    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    hour = str(now.hour)
    minn = str(now.minute)
    sec = str(now.second)
    
    if len(day) == 1:
        day = '0' + day
    if len(month) == 1:
        month = '0' + month
    if len(hour) == 1:
        hour = '0' + month
    if len(minn) == 1:
        minn = '0' + month
    if len(sec) == 1:
        sec = '0' + month
    return year, month, day, hour, minn, sec

def writeFile(raw, filename):
    newfile = open(filename, 'wb')
    newfile.write(raw)
    newfile.close()

def main():
    global flagDebug, flagReset
    args = cmdArgsParser()
    #flagDebug = int(args.flagDebug)
    
    if(args.getcfg):
        if flagDebug > 1: print "Get Config from Alteon"
        getCfgAlteon()
    if(args.flagReset):
        flagReset = int(args.flagReset)
        if flagDebug > 1: print "Flag Reset : ", flagReset
        if(flagReset == 0):
            if flagDebug > 1: print "Reset all Alteons"
        rstAlteon()
        
    sys.exit()

if __name__ == '__main__':    
#    if secret == "": secret = getpass.getpass('Password:')   
    print "Begin Programm ..."
    sys.exit(main())

