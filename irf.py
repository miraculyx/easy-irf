#!/usr/bin/python
import comware, sys, getopt, re

# Author      : Ing. G. H. Lange
# Date        : 15/07/2016
# Description : Python script for simplifying the IRF Setup on HPN5130 switches

script_name = sys.argv[0] 
script_name = re.sub(r'(^.*[\\/])', '', script_name)
usage = 'Usage: python ' + script_name +' <irf member id> <irf-port number> <IF number> [Ten-GigabitEthernet|FortyGigE]' + '\r\n  [] : optional parameters'

if (len(sys.argv) == 1 or len(sys.argv) > 5):
   print usage
   sys.exit(1)
  
if  (len(sys.argv) == 2 ):
   member = sys.argv[1]  
   irfportid = 1
   port = 12
   media = 'Ten-GigabitEthernet'
else:
   member = sys.argv[1]   
   irfportid = sys.argv[2]   
   port = sys.argv[3]  
   media = 'Ten-GigabitEthernet'
 
if (int(member) == 0):
   print usage
   sys.exit(1)
  
if  (len(sys.argv) == 5 ):
   member = sys.argv[1]   
   irfportid = sys.argv[2]   
   port = sys.argv[3]  
   media = sys.argv[4]  
 
media = media[0].upper()

# Do not print comware.CLI output
PRINT_OUTPUT = False

def irf_port(member,media,irfportid,portid):
   if  (media == 'F'):
      mtype='FortyGigE'
   else:
      mtype='Ten-GigabitEthernet'
   port = mtype + member + '/0/' + str(portid)
   irfport = 'irf-port ' + str(member) + '/' + str(irfportid)
   command = 'system-view ; irf member ' + str(member) + ' priority ' + str(int(33)-int(member))
   comware.CLI(command,PRINT_OUTPUT)
   comware.CLI('system-view ; interface ' + port + ' ; description IRF-PORT ; shutdown',PRINT_OUTPUT)	
   comware.CLI('system-view ; ' + irfport + ' ; port group interface ' + port,PRINT_OUTPUT)
   comware.CLI('system-view ; irf-port-configuration active',PRINT_OUTPUT)
   comware.CLI('system-view ; interface ' + port + ' ; description IRF-PORT ; undo shutdown',PRINT_OUTPUT)		
   command = 'system-view ; irf member ' + str(member) + ' description SW' + str(member)
   comware.CLI(command,PRINT_OUTPUT)
   comware.CLI('save force',PRINT_OUTPUT)	
   return port   

# Verify which IRF ID we have 
irfid = int(comware.get_self_slot()[1])

if int(member) == int(irfid):  
   print 'Actual IRF Member ID is ' + str(member)
   irfport = irf_port(str(member), media, str(irfportid), str(port))
   print 'Bound interface ' + irfport + ' to irf-port' + str(member) + '/' + str(irfportid)
else:
   print 'Changing the IRF ID to ' + str(member)
   command = 'system-view ; irf member ' + str(irfid) + ' renumber ' + str(member) + ' ;'
   comware.CLI(command,PRINT_OUTPUT)
   print 'Rebooting now ...'
   comware.CLI('reboot',PRINT_OUTPUT)
  
  