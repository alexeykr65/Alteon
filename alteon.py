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

ALTEON = "192.168.180.61"
USER = "admin"
PASSWORD = "admin"
myAuth=requests.auth.HTTPBasicAuth(USER, PASSWORD)


description = "alteon: Get information from Alteon"
epilog = "ciscoblog.ru"

listParamConfig = ['internal_interface','internal_lan','external_interface']
flagDebug = int()
flagL2vpn = int()
sterraConfig = dict()
flagFullMesh = 0
flagCentral = 1

fileName = ""
keyPreShare = ""
nameInterface = ""

def getCfgAlteon():
    global ALTEON, USER, PASSWORD, myAuth, flagDebug
    myAuth=requests.auth.HTTPBasicAuth(USER, PASSWORD)
    reqSTR =  "https://"+ALTEON+"/config/getcfg"
    requests.packages.urllib3.disable_warnings()
    r = requests.get(reqSTR, auth=myAuth, verify=False)
    rr = zlib.decompress(r.content, zlib.MAX_WBITS|32)
    print "Config Alteon: \n " + rr
    
def cmdArgsParser():
    global fileName, keyPreShare, nameInterface, flagDebug, flagFullMesh, flagL2vpn
    if flagDebug > 0: print "Analyze options ... "
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('-f', '--file', help='File name with source data', dest="fileName", default = 'sterra.conf')
    parser.add_argument('-c', '--getcfg', help='Get Config From Alteon', action="store_true")
    parser.add_argument('-i', '--interface', help='Name of interfaces (default GigabitEthernet)', action="store",  dest="nameInterface", default="GigabitEthernet")
    parser.add_argument('-d', '--debug', help='Debug information view(default =1, 2- more verbose', dest="flagDebug", default=1)
    parser.add_argument('-m', '--mesh', help='Enable Full Mesh(default = disable', action="store_true")
    parser.add_argument('-l2', '--l2vpn', help='Generate configuration for L2 VPN', action="store_true")
    flagDebug = 2
    return parser.parse_args()


def main():
    global flagDebug
    args = cmdArgsParser()
    print "Begin module Main \n"
    
    if(args.getcfg):
        if flagDebug > 1: print " Module Main, args - getcfg\n"
        getCfgAlteon()
     
    # Kill vm with PIDs
    # PowerON vm with PIDs
    
    sys.exit()

if __name__ == '__main__':
    
#    if secret == "": secret = getpass.getpass('Password:')
    
    print "Begin Programm \n"
    sys.exit(main())

