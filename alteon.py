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
import glob
from StringIO import StringIO
import datetime
import tarfile
import time
import json



listAlteon = ['192.168.180.61', '192.168.180.62',
              '192.168.180.63', '192.168.180.64']
altUser = "admin"
altPass = "admin"
myAuth = requests.auth.HTTPBasicAuth(altUser, altPass)
dirConfigFiles = ''
description = "alteon: Get and Set Information from Alteon"
epilog = "http://ciscoblog.ru, http://github.com/alexeykr65/Alteon"

flagDebug = 1
flagReset = int()
paramListAlteon = list()
captureDo = str()

fileName = ""
keyPreShare = ""
nameInterface = ""


def getCfgAlteon():
    global flagDebug
    writeDebugMsg("Get Config from Alteons ...", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 1)
        reqUrl = "https://" + sAlteon + "/config/getcfg"
        r = getRequests(reqUrl, 1, "")
        if(r):
            year, month, day, hour, minn, sec = getDate()
            fileName = '-'.join(["Alteon", sAlteon, "config", year, month, day, hour, minn, sec + ".txt"])
            writeDebugMsg(" Filename cfg: " + fileName, 2)
            tar = tarfile.open(fileobj=StringIO(r.content), mode="r:gz")
            tar.extractall()
            tar.close()
            os.rename("altconfig.txt", dirConfigFiles + "/" + fileName)


def setCfgAlteon():
    global flagDebug, dirConfigFiles
    writeDebugMsg("Config from directory: " + dirConfigFiles, 1)
    for fileDir in glob.glob1(dirConfigFiles, "*.txt"):
        targetAlteon = fileDir.split('-')
        sAlteon = targetAlteon[1]
        if sAlteon in listAlteon:
            writeDebugMsg("Config File: " + fileDir, 1)
            writeDebugMsg("Import to alteon: " + sAlteon, 1)
            tar = tarfile.open("./altconfig.tgz", mode="w:gz")
            fileForTar = dirConfigFiles + "/" + fileDir
            tar.add(name=fileForTar, arcname='altconfig.txt')
            tar.close()
            reqUrl = "https://" + sAlteon + "/config/configimport?pkey=no"
            # data = open("./altconfig.tgz", 'rb').read()
            res = getRequests(reqUrl, 4, 'altconfig.tgz', 120)
            # res = requests.post(url=reqUrl, data=data, headers={'Content-Type': 'application/octet-stream'}, auth=myAuth, verify=False, timeout=120)
            # data.close()
            #        r = getRequests(reqUrl, 3, "./altconfig.tgz")
            # 'authorization: Basic YWRtaW46YWRtaW4='
            print "Return from Alteon : " + res.content


def rstAlteon():
    global flagDebug, flagReset
    writeDebugMsg("Reset Alteon ... ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 1)
        reqUrl = "https://" + sAlteon + "/config"
        getRequests(reqUrl, 2, '{"agReset":"2"}')


def rstConfigAlteon():
    global flagDebug, flagReset
    writeDebugMsg("Reset Config Alteon ... ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 1)
        reqUrl = "https://" + sAlteon + "/config"
        getRequests(reqUrl, 2, '{"agConfigForNxtReset":"4"}')


def realServerStatistic():
    global flagDebug, flagReset
    writeDebugMsg("Get Real Server Statistic ... ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 1)
        reqUrl = "https://" + sAlteon + "/config/SlbStatEnhRServerTable"
        slbRes = getRequests(reqUrl, 1, '')
        reqUrl = "https://" + sAlteon + "/config/SlbEnhRealServerInfoTable"
        realSrvRes = getRequests(reqUrl, 1, '')
        jsonSlbRes = json.loads(slbRes.content)
        jsonRealSrvRes = json.loads(realSrvRes.content)
        # print realSrvRes.content
        srvInfo = jsonRealSrvRes['SlbEnhRealServerInfoTable']
        slbTable = jsonSlbRes['SlbStatEnhRServerTable']
        print ("%5s %16s %10s %10s %10s %30s" % ("Index", "IPaddr", "CurSess", "TotalSess", "HighSess", "Uptime"))
        intCount = 0
        for sDat in slbTable:
            if(sDat['CurrSessions'] > 0 or sDat['TotalSessions'] > 0 or sDat['HighestSessions'] > 0):
                print ("%5s %16s %10s %10s %10s %30s" % (sDat['Index'], srvInfo[intCount]['IpAddr'], sDat['CurrSessions'], sDat['TotalSessions'], sDat['HighestSessions'], srvInfo[intCount]['UpTime']))
            intCount = intCount + 1
        #           print sDat['Index'], sDat['CurrSessions'], sDat['TotalSessions'], sDat['HighestSessions']


def virtServerStatistic():
    global flagDebug, flagReset
    writeDebugMsg("Get Real Server Statistic ... ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 1)
        reqUrl = "https://" + sAlteon + "/config/SlbCurCfgEnhVirtServicesTable"
#        slbRes = getRequests(reqUrl, 1, '')
#        reqUrl = "https://" + sAlteon + "/config/SlbEnhRealServerInfoTable"
        virtSrvRes = getRequests(reqUrl, 1, '')
        jsonVirtRes = json.loads(virtSrvRes.content)
        virtInfo = jsonVirtRes['SlbCurCfgEnhVirtServicesTable']
        print ("%5s %16s %10s %10s %10s" % ("VirtInd", "VirtPort", "CurSess", "TotalSess", "HighSess"))
        intCount = 0
        for sDat in virtInfo:
            print ("%5s %16s %10s %10s %10s" % (sDat['ServIndex'], sDat['VirtPort'], sDat['CurrSessions'], sDat['TotalSessions'], sDat['HighestSessions']))
            intCount = intCount + 1


def virtServiceServerStatistic():
    global flagDebug, flagReset
    writeDebugMsg("Get Real Server Statistic ... ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 1)
        reqUrl = "https://" + sAlteon + "/config/SlbEnhStatVirtServiceTable"
        virtSrvRes = getRequests(reqUrl, 1, '')
        jsonVirtRes = json.loads(virtSrvRes.content)
        virtInfo = jsonVirtRes['SlbEnhStatVirtServiceTable']
        print ("%5s %10s %16s %10s %10s %10s" % ("VirtInd", "Service", "Server", "CurSess", "TotalSess", "HighSess"))
        srvInfo = getServerTable(sAlteon)
        for sDat in virtInfo:
            if(sDat['CurrSessions'] > 0 or sDat['TotalSessions'] > 0 or sDat['HighestSessions'] > 0):
                print ("%5s  %10s  %16s %10s %10s %10s" % (sDat['ServerIndex'], sDat['Index'], srvInfo[sDat['RealServerIndex']], sDat['CurrSessions'], sDat['TotalSessions'], sDat['HighestSessions']))


def getServerTable(sAlteon):
    global flagDebug, flagReset
    srvInfo = dict()
    writeDebugMsg("Get Real Server Information ... ", 2)
    writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
    reqUrl = "https://" + sAlteon + "/config/SlbEnhRealServerInfoTable"
    virtSrvRes = getRequests(reqUrl, 1, '')
    jsonVirtRes = json.loads(virtSrvRes.content)
    virtInfo = jsonVirtRes['SlbEnhRealServerInfoTable']
    for sDat in virtInfo:
#        print ("%5s %16s" % (sDat['Index'], sDat['IpAddr']))
        srvInfo[sDat['Index']] = sDat['IpAddr']
    return srvInfo


def setTimeDate():
    global flagDebug, flagReset
    writeDebugMsg("Set time and date on Alteons ...", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 1)
        reqUrl = "https://" + sAlteon + "/config"
        year, month, day, hour, minn, sec = getDate()
        setTime = '{"agRtcTime":"' + ':'.join([hour, minn, sec]) + '"}'
        writeDebugMsg("Set timezone on Alteon ...", 1)
        getRequests(reqUrl, 2, '{"agNewCfgNTPTzoneHHMM":"+03:00"}')
        writeDebugMsg("Apply changes on Alteon ...", 1)
        getRequests("https://" + sAlteon + "/config?action=apply", 2, '')
        writeDebugMsg("Waiting apply ...", 1)
        time.sleep(100)
        writeDebugMsg("Set time ...", 1)
        getRequests(reqUrl, 2, setTime)
        setDate = '{"agRtcDate":"' + '/'.join([month, day, year]) + '"}'
        writeDebugMsg("Set date on Alteons ...", 1)
        getRequests(reqUrl, 2, setDate)


def shtAlteon():
    global flagDebug, flagReset
    writeDebugMsg("Shutdown Alteons ... ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 1)
        reqUrl = "https://" + sAlteon + "/config"
        getRequests(reqUrl, 2, '{"agShutdown":"2"}')


def saveConfig():
    global flagDebug, flagReset
    writeDebugMsg("Save Config on Alteons ... ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 1)
        reqUrl = "https://" + sAlteon + "/config?action=save"
        getRequests(reqUrl, 2, '')


def applyConfig():
    global flagDebug, flagReset
    writeDebugMsg("Apply Config on Alteons ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 1)
        reqUrl = "https://" + sAlteon + "/config?action=apply"
        getRequests(reqUrl, 2, '')


def capConfig():
    global flagDebug, flagReset, captureDo
    writeDebugMsg("Capture start on Alteon ...  ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        reqUrl = "https://" + sAlteon + "/config/pktcapture?cmd=" + captureDo
        r = getRequests(reqUrl, 1, '')
        print "Respond Text: " + r.content


def exportCapture():
    global flagDebug
    writeDebugMsg("Export Capture file ...  ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        writeDebugMsg("Try to export capture file ... ", 2)
        reqUrl = "https://" + sAlteon + "/config/getcapturefile"
        r = getRequests(reqUrl, 1, "")
        if(r):
            tar = tarfile.open(fileobj=StringIO(r.content), mode="r:gz")
            writeDebugMsg(tar.list(), 1)
            tar.extractall()
            tar.close()


def getLogFile():
    global flagDebug
    writeDebugMsg("Export Logging file ... ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        writeDebugMsg("Try to get log file ... ", 2)
        reqUrl = "https://" + sAlteon + "/config/getapplog"
        r = getRequests(reqUrl, 1, "")
        if(r):
            tar = tarfile.open(fileobj=StringIO(r.content), mode="r:gz")
            writeDebugMsg(tar.list(), 1)
            tar.extractall()
            tar.close()


def diffConfig():
    global flagDebug, flagReset
    writeDebugMsg("Diff Config  ", 1)
    for sAlteon in listAlteon:
        writeDebugMsg("Alteon Ip address: " + sAlteon, 2)
        reqUrl = "https://" + sAlteon + "/config/getdiff"
        r = getRequests(reqUrl, 1, '')
        writeDebugMsg("Diff apply config: " + str(r.content), 1)
        reqUrl = "https://" + sAlteon + "/config/getdiffflash"
        r = getRequests(reqUrl, 1, '')
        writeDebugMsg("Diff flash config: " + str(r.content), 1)


def getRequests(pReqUrl, pMethod, pParam, pTimeout=10):
    global myAuth, flagDebug
    # writeDebugMsg("===================================================", 1)
    requests.packages.urllib3.disable_warnings()
    count = 4
    while(count > 1):
        try:
            if(pMethod == 1):
                r = requests.get(pReqUrl, auth=myAuth, verify=False, timeout=pTimeout)
                writeDebugMsg("URL string : " + pReqUrl, 3)
            elif(pMethod == 2):
                if(pParam):
                    writeDebugMsg("Http POST parameters : " + pParam, 1)
                writeDebugMsg("URL string : " + pReqUrl, 3)
                r = requests.put(pReqUrl, auth=myAuth, verify=False, timeout=pTimeout, data=pParam)
            elif(pMethod == 3):
                writeDebugMsg("URL string : " + pReqUrl, 3)
                r = requests.post(pReqUrl, auth=myAuth, verify=False, timeout=pTimeout)
            elif(pMethod == 4):
                writeDebugMsg("URL string : " + pReqUrl, 3)
                files = {'file': open(pParam, 'rb')}
                r = requests.post(pReqUrl, auth=myAuth, verify=False, timeout=pTimeout, files=files)

        except requests.ConnectionError, e:
            print "Error : ", e
            return 0
        if(r.status_code == 200):
            writeDebugMsg("Respond Status: " + str(r.status_code), 2)
            count = 0
        else:
            count = count - 1
            writeDebugMsg("Respond Status: " + str(r.status_code) + " , and try again ...", 2)
    # writeDebugMsg("Return string: " + str(r.content), 2)
    return r


def cmdArgsParser():
    global fileName, keyPreShare, nameInterface, flagDebug, flagFullMesh, flagL2vpn, dirConfigFiles

    writeDebugMsg("Analyze command line options ... ", 1)
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('-l', '--listalteon', help='List of Alteons(ex:\'192.168.1.61,192.168.1.62\')', action="store", dest="listalteon")
    # parser.add_argument('-f', '--file', help='File name with source data', dest="fileName", default='sterra.conf')
    parser.add_argument('-cdir', '--cfgdir', help='Conf Alteon directory(default conf)', action="store", dest="cfgdir", default="conf")
    parser.add_argument('-ec', '--exportcfg', help='Export Config From Alteon', action="store_true")
    parser.add_argument('-ic', '--importcfg', help='Import Config to Alteon', action="store_true")
    parser.add_argument('-r', '--reset', help='Reset(reboot) Alteons', action="store_true")
    parser.add_argument('-s', '--shutdown', help='Shutdown Alteons', action="store_true")
    parser.add_argument('-cr', '--cfgreset', help='Reset Configuration Alteons', action="store_true")
    parser.add_argument('-cs', '--save', help='Save Config on Alteons', action="store_true")
    parser.add_argument('-ca', '--apply', help='Apply Config on Alteons', action="store_true")
    parser.add_argument('-cd', '--diff', help='Diff Config on Alteons', action="store_true")
    parser.add_argument('-cp', '--capture', help='Capture Traffic on Alteons', action="store", dest="capture", default="")
    parser.add_argument('-ecp', '--exportcapture', help='Export File Capture from Alteons', action="store_true")
    parser.add_argument('-lg', '--getlog', help='Export Logging File from Alteons', action="store_true")
    parser.add_argument('-st', '--settime', help='Set time and date on Alteons', action="store_true")
    parser.add_argument('-mr', '--realserver', help='Get Stat Real Server ', action="store_true")
    parser.add_argument('-mv', '--virtserver', help='Get Stat Virt Server ', action="store_true")
    parser.add_argument('-ms', '--virtservice', help='Get Stat Virt Service with Server ', action="store_true")
    parser.add_argument('-d', '--debug', help='Debug information view(default =1, 2- more verbose', dest="flagDebug", default=1)

    if(len(sys.argv) < 2):
        parser.print_help()
        exit(1)
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
        hour = '0' + hour
    if len(minn) == 1:
        minn = '0' + minn
    if len(sec) == 1:
        sec = '0' + sec
    return year, month, day, hour, minn, sec


def writeFile(raw, filename):
    newfile = open(filename, 'wb')
    newfile.write(raw)
    newfile.close()


def writeDebugMsg(sMsg, levelDebug):
    global flagDebug
    if flagDebug >= levelDebug:
        print sMsg


def main():
    global flagDebug, flagReset, paramListAlteon, listAlteon, captureDo, dirConfigFiles
    args = cmdArgsParser()
    flagDebug = int(args.flagDebug)
    dirConfigFiles = args.cfgdir
    if(args.listalteon):
        paramListAlteon = list(args.listalteon.split(','))
        listAlteon = list(args.listalteon.split(','))
        writeDebugMsg("listAlteon : " + " ".join(listAlteon), 2)

    if(args.exportcfg):
        getCfgAlteon()
    if(args.importcfg):
        writeDebugMsg("Import Config to Alteon", 2)
        setCfgAlteon()
    if(args.cfgreset):
        rstConfigAlteon()
        # rstAlteon()
    if(args.reset):
        rstAlteon()
    if(args.shutdown):
        shtAlteon()
    if(args.save):
        saveConfig()
    if(args.apply):
        applyConfig()
    if(args.diff):
        diffConfig()
    if(args.capture):
        captureDo = args.capture
        capConfig()
    if(args.exportcapture):
        exportCapture()
    if(args.getlog):
        getLogFile()
    if(args.settime):
        setTimeDate()
    if(args.realserver):
        realServerStatistic()
    if(args.virtserver):
        virtServerStatistic()
    if(args.virtservice):
            virtServiceServerStatistic()

    sys.exit()


if __name__ == '__main__':
    # if secret == "": secret = getpass.getpass('Password:')
    print "Begin Programm ..."
    sys.exit(main())
