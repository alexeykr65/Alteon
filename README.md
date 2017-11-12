# Alteon Configuration Monitoring

usage: alteon.py [-h] [-l LISTALTEON] [-cdir CFGDIR] [-ec] [-ic] [-r] [-s]
                 [-cr] [-cs] [-ca] [-cd] [-cp CAPTURE] [-ecp] [-lg] [-st]
                 [-mr] [-mv] [-d FLAGDEBUG]

alteon: Get and Set Information from Alteon

optional arguments:
  -h, --help            show this help message and exit
  -l LISTALTEON, --listalteon LISTALTEON
                        List of Alteons(ex:'192.168.1.61,192.168.1.62')
  -cdir CFGDIR, --cfgdir CFGDIR
                        Conf Alteon directory(default conf)
  -ec, --exportcfg      Export Config From Alteon
  -ic, --importcfg      Import Config to Alteon
  -r, --reset           Reset(reboot) Alteons
  -s, --shutdown        Shutdown Alteons
  -cr, --cfgreset       Reset Configuration Alteons
  -cs, --save           Save Config on Alteons
  -ca, --apply          Apply Config on Alteons
  -cd, --diff           Diff Config on Alteons
  -cp CAPTURE, --capture CAPTURE
                        Capture Traffic on Alteons
  -ecp, --exportcapture
                        Export File Capture from Alteons
  -lg, --getlog         Export Logging File from Alteons
  -st, --settime        Set time and date on Alteons
  -mr, --realserver     Get Stat Real Server
  -mv, --virtserver     Get Stat Virt Server
  -d FLAGDEBUG, --debug FLAGDEBUG
                        Debug information view(default =1, 2- more verbose

http://ciscoblog.ru, http://github.com/alexeykr65/Alteon
