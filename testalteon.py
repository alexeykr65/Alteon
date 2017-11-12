#!/usr/bin/env python
#
# Get configuration for Alteon
#
# alexeykr@gmail.com
#
import sys
import argparse
import requests
import re
import time




listAlteon = ['192.168.180.65', '192.168.180.66']
description = "alteon: Get and Set Information from Alteon"
epilog = "http://ciscoblog.ru, http://github.com/alexeykr65/Alteon"

flagDebug = 1
flagReset = int()
paramListAlteon = list()
captureDo = str()

fileName = ""
keyPreShare = ""
nameInterface = ""


def getRequests(pReqUrl, pTimeout=10):
    global myAuth, flagDebug
    # writeDebugMsg("===================================================", 1)
    requests.packages.urllib3.disable_warnings()
    headers = {'user-agent': 'my-app/0.0.2'}
    try:
        r = requests.get(pReqUrl, verify=False, timeout=pTimeout, headers=headers)
    except requests.ConnectionError, e:
        print "Error : ", e
        return 0
    if(r.status_code == 200):
        for sT in r.text.split('\n'):
            m = re.search("Success", sT)
            if(m):
                print sT
    return r


def writeDebugMsg(sMsg, levelDebug):
    global flagDebug
    if flagDebug >= levelDebug:
        print sMsg


def cmdArgsParser():
    global fileName, keyPreShare, nameInterface, flagDebug, flagFullMesh, flagL2vpn, dirConfigFiles

    writeDebugMsg("Analyze command line options ... ", 1)
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('-l', '--listalteon', help='List of Alteons(ex:\'192.168.1.61,192.168.1.62\')', action="store", dest="listalteon")
    parser.add_argument('-n', '--numrepeat', help='Number of repeat get', action="store", dest="numrepeat", default=10)
    parser.add_argument('-s', '--numsec', help='Interval in sec', action="store", dest="numsec", default=0)
    # parser.add_argument('-f', '--file', help='File name with source data', dest="fileName", default='sterra.conf')
    #parser.add_argument('-cdir', '--cfgdir', help='Conf Alteon directory(default conf)', action="store", dest="cfgdir", default="conf")
    #parser.add_argument('-ec', '--exportcfg', help='Export Config From Alteon', action="store_true")
    #parser.add_argument('-ic', '--importcfg', help='Import Config to Alteon', action="store_true")
    #parser.add_argument('-r', '--reset', help='Reset(reboot) Alteons', action="store_true")
    #parser.add_argument('-s', '--shutdown', help='Shutdown Alteons', action="store_true")
    #parser.add_argument('-cr', '--cfgreset', help='Reset Configuration Alteons', action="store_true")
    #parser.add_argument('-cs', '--save', help='Save Config on Alteons', action="store_true")
    #parser.add_argument('-ca', '--apply', help='Apply Config on Alteons', action="store_true")
    #parser.add_argument('-cd', '--diff', help='Diff Config on Alteons', action="store_true")
    #parser.add_argument('-cp', '--capture', help='Capture Traffic on Alteons', action="store", dest="capture", default="")
    #parser.add_argument('-ecp', '--exportcapture', help='Export File Capture from Alteons', action="store_true")
    #parser.add_argument('-lg', '--getlog', help='Export Logging File from Alteons', action="store_true")
    #parser.add_argument('-st', '--settime', help='Set time and date on Alteons', action="store_true")
    #parser.add_argument('-mr', '--realserver', help='Get Stat Real Server ', action="store_true")
    #parser.add_argument('-mv', '--virtserver', help='Get Stat Virt Server ', action="store_true")
    parser.add_argument('-d', '--debug', help='Debug information view(default =1, 2- more verbose', dest="flagDebug", default=2)

    if(len(sys.argv) < 2):
        parser.print_help()
        exit(1)
    return parser.parse_args()


def main():
    global flagDebug, flagReset, paramListAlteon, listAlteon, captureDo, dirConfigFiles
    args = cmdArgsParser()
    flagDebug = int(args.flagDebug)
    numRepeat = int(args.numrepeat)
    numSec = int(args.numsec)
    if(args.listalteon):
        paramListAlteon = list(args.listalteon.split(','))
        listAlteon = list(args.listalteon.split(','))
        writeDebugMsg("listAlteon : " + " ".join(listAlteon), 2)

    for sAlteon in listAlteon:
        reqUrl = "http://" + sAlteon
        for x in range(numRepeat):
            writeDebugMsg("Ip address: " + sAlteon + "  Index : " + str(x), 1)
            getRequests(reqUrl)
            if(numSec > 0):
                time.sleep(numSec)

    sys.exit()


if __name__ == '__main__':
    # if secret == "": secret = getpass.getpass('Password:')
    print "Begin Programm ..."
    sys.exit(main())
