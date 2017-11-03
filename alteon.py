#!/usr/bin/env python
#
# Get configuration for Alteon
#
# alexeykr@gmail.com
#
import sys
import argparse
import requests
import os
from StringIO import StringIO
import datetime
import tarfile


listAlteon = ['192.168.180.61', '192.168.180.62', '192.168.180.63', '192.168.180.64']
altUser = "admin"
altPass = "admin"
myAuth = requests.auth.HTTPBasicAuth(altUser, altPass)

description = "alteon: Get and Set Information from Alteon"
epilog = "ciscoblog.ru"

flagDebug = int()
flagReset = int()
paramListAlteon = list()
captureDo = str()

fileName = ""
keyPreShare = ""
nameInterface = ""


def getCfgAlteon():
    global flagDebug

    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        reqUrl = "https://"+sAlteon+"/config/getcfg"
        r = getRequests(reqUrl, 1, "")
        if(r):
            year, month, day, hour, minn, sec = getDate()
            fileName = '-'.join(["Alteon", sAlteon, "config", year, month, day, hour, minn, sec + ".txt"])
            writeDebugMsg(" Filename cfg: " + fileName, 2)
            tar = tarfile.open(fileobj=StringIO(r.content), mode="r:gz")
            tar.extractall()
            tar.close()
            os.rename("altconfig.txt", fileName)


def rstAlteon():
    global flagDebug, flagReset

    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        reqUrl = "https://"+sAlteon+"/config"
        getRequests(reqUrl, 2, '{"agReset":"2"}')


def shtAlteon():
    global flagDebug, flagReset

    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        reqUrl = "https://"+sAlteon+"/config"
        getRequests(reqUrl, 2, '{"agShutdown":"2"}')


def saveConfig():
    global flagDebug, flagReset

    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        reqUrl = "https://"+sAlteon+"/config?action=save"
        getRequests(reqUrl, 2, '')


def applyConfig():
    global flagDebug, flagReset

    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        reqUrl = "https://"+sAlteon+"/config?action=apply"
        getRequests(reqUrl, 2, '')


def capConfig():
    global flagDebug, flagReset, captureDo

    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        reqUrl = "https://" + sAlteon + "/config/pktcapture?cmd=" + captureDo
        r = getRequests(reqUrl, 1, '')
        print "Respond: " + r.content


def exportCapture():
    global flagDebug

    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        writeDebugMsg("Try to export capture file ... ", 2)
        reqUrl = "https://"+sAlteon+"/config/getcapturefile"
        r = getRequests(reqUrl, 1, "")
        if(r):
            tar = tarfile.open(fileobj=StringIO(r.content), mode="r:gz")
            writeDebugMsg(tar.list(), 1)
            tar.extractall()
            tar.close()


def diffConfig():
    global flagDebug, flagReset

    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        reqUrl = "https://"+sAlteon+"/config/getdiff"
        r = getRequests(reqUrl, 1, '')
        writeDebugMsg("Diff apply config: " + str(r.content), 1)
        reqUrl = "https://"+sAlteon+"/config/getdiffflash"
        r = getRequests(reqUrl, 1, '')
        writeDebugMsg("Diff flash config: " + str(r.content), 1)


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
            elif(pMethod == 3):
                r = requests.post(pReqUrl, auth=myAuth, verify=False, timeout=10)
        except requests.ConnectionError, e:
            print "Error : ", e
            return 0
        if(r.status_code == 200):
            writeDebugMsg(" Status: " + str(r.status_code), 2)
            count = 0
        else:
            count = count - 1
            writeDebugMsg(" Status else: " + str(r.status_code), 2)
    return r


def cmdArgsParser():
    global fileName, keyPreShare, nameInterface, flagDebug, flagFullMesh, flagL2vpn
    writeDebugMsg("Analyze options ... ", 1)
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('-f', '--file', help='File name with source data', dest="fileName", default='sterra.conf')
    parser.add_argument('-cg', '--getcfg', help='Get Config From Alteon', action="store_true")
    parser.add_argument('-r', '--reset', help='Reset Alteons', action="store_true")
    parser.add_argument('-sh', '--shutdown', help='Shutdown Alteons', action="store_true")
    parser.add_argument('-cs', '--save', help='Save Config on Alteons', action="store_true")
    parser.add_argument('-ca', '--apply', help='Apply Config on Alteons', action="store_true")
    parser.add_argument('-cd', '--diff', help='Diff Config on Alteons', action="store_true")
    parser.add_argument('-ce', '--capexport', help='Capture export from Alteons', action="store_true")
    parser.add_argument('-cp', '--capture', help='Capture Traffic Alteons', action="store",  dest="capture", default="")
    parser.add_argument('-l', '--listalteon', help='List of Alteons', action="store",  dest="listalteon", default='')
    parser.add_argument('-d', '--debug', help='Debug information view(default =1, 2- more verbose', dest="flagDebug", default=1)
    parser.add_argument('-m', '--mesh', help='Enable Full Mesh(default = disable', action="store_true")
    parser.add_argument('-l2', '--l2vpn', help='Generate configuration for L2 VPN', action="store_true")
    flagDebug = 2
    return parser.parse_args()


def getDate():
    # Get Date create file Name
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


def writeDebugMsg(sMsg, levelDebug):
    if flagDebug >= levelDebug:
        print sMsg


def main():
    global flagDebug, flagReset, paramListAlteon, listAlteon, captureDo
    args = cmdArgsParser()
    # flagDebug = int(args.flagDebug)
    if(args.listalteon):
        paramListAlteon = list(args.listalteon.split(','))
        listAlteon = list(args.listalteon.split(','))
        writeDebugMsg("listAlteon : " + " ".join(listAlteon), 2)

    if(args.getcfg):
        writeDebugMsg("Get Config from Alteon", 2)
        getCfgAlteon()
    if(args.reset):
        writeDebugMsg("Flag Reset enable ", 2)
        rstAlteon()
    if(args.shutdown):
        writeDebugMsg("Flag Shutdown enable ", 2)
        shtAlteon()
    if(args.save):
        writeDebugMsg("Flag Save Config ", 2)
        saveConfig()
    if(args.apply):
        writeDebugMsg("Flag Apply Config ", 2)
        applyConfig()
    if(args.diff):
        writeDebugMsg("Diff Config  ", 2)
        diffConfig()
    if(args.capture):
        writeDebugMsg("Capture Config  ", 2)
        captureDo = args.capture
        capConfig()
    if(args.capexport):
        writeDebugMsg("Export Capture file  ", 2)
        exportCapture()

    sys.exit()


if __name__ == '__main__':
    # if secret == "": secret = getpass.getpass('Password:')
    print "Begin Programm ..."
    sys.exit(main())
