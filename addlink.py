#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import apiguifi
import sys,getopt
from env import *


def main(argv):
   node_name=""
   test = False
   node_id = ""
   ap_id = ""
   dev_name = ""
   mac = "00:00:00:00:00:00"
   model_id = "101"
   def help():
      print('Usage: addlink.py -h -t -n node_id -a ap_id -d device_name [-m MAC] [-i model_id]' )
      print('Links node identified by node_id to device_id AP.')
      print('	-h, --help		Display help and exit')
      print('	-t, --test		Use test.guifi.net instead of production website')
      print('	-n, --node_id		ID of the node to link')
      print('	-a, --ap_id		ID of the device of the AP to link to')
      print('	-d, --device_name	Name of the device of the node to link from (will be created)')
      print('   -m, --mac		MAC of the new device. Optional. Default 00:00:00:00:00:00')
      print('   -i, --model_id		Model ID of the new device. Optional. Default 101 (SXTG-5HPacD). Also avail 70 (Routerboard SXT Lite5)  Check out printmodels.py')

   try:
      opts, args = getopt.getopt(argv,"htn:a:d:m:i:",["node_id=","ap_id=","device_name=","mac=","model_id="])
   except getopt.GetoptError:
      help()
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         help()
         sys.exit()
      elif opt in ("-t", "--test"):
         test = True
      elif opt in ("-n", "--node_id"):
         node_id = arg
      elif opt in ("-a", "--ap_id"):
         ap_id = arg
      elif opt in ("-d", "--device_name"):
         dev_name = arg
      elif opt in ("-m", "--mac"):
         mac = arg
      elif opt in ("-i", "--model_id"):
         model_id = arg
   if dev_name == "" or ap_id == "":
      help()
      sys.exit(2)

   radiodev_counter0=0
   radiodev_counter1=0
   g=apiguifi.apiguifi(test)
   g.login(username,password)

   dev_id = g.add_device({"model_id":model_id, "firmware":"RouterOSv6.x","nick":dev_name,"mac":mac,"node_id":node_id,"type":"radio"})
   radiodev_counter0 = g.add_radio({"mode":"client","device_id":dev_id,"mac":mac,"antenna_gain":14})
   near_aps = g.get_near_ap(node_id)
   for i in near_aps:
      if ap_id == i['device_id']:
         radiodev_counter1=i['radiodev_counter']
         break;
   g.add_link_to_AP(dev_id,ap_id,radiodev_counter0,radiodev_counter1)
   print("Link added successfully")

if __name__ == "__main__":
   main(sys.argv[1:])



