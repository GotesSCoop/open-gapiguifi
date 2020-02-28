#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import apiguifi
import sys,getopt
from env import *


def main(argv):
   node_name=""
   test = False
   lat = ""
   lon = ""
   ap = "null"
   zone = 41583
   def help():
      print('Usage: addnode.py -h -t -n node_name -l lat -L lon [-z zone]')
      print('Adds node at geographic location identified by lat and lon options. If device_id passed, links this to device_id AP.')
      print('	-h, --help		Display help and exit')
      print('	-t, --test		Use test.guifi.net instead of production website')
      print('	-n, --name		Name of the new node')
      print('	-l, --lat		Latitude of the new node (float)')
      print('	-L, --lon		Longitude of the new node (float)')
      print('	-z, --zone		Zone ID of the new node. Optional. Default 41583 (Sóller)')
   try:
      opts, args = getopt.getopt(argv,"htn:l:L:z:m:",["name=","lat=","lon=","zone=","mac="])
   except getopt.GetoptError:
      help()
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         help()
         sys.exit()
      elif opt in ("-t", "--test"):
         test = True
      elif opt in ("-n", "--name"):
         node_name = arg
      elif opt in ("-l", "--lat"):
         lat = arg
      elif opt in ("-L", "--lon"):
         lon = arg
      elif opt in ("-z", "--zone"):
         zone = arg
   if node_name == "" or lat == "" or lon == "":
      print("Missing parameters node_name, lat or lon")
      help()
      sys.exit(2)

   g=apiguifi.apiguifi(test)
   g.login(username,password)
   node_id=g.add_node({"title":node_name,"zone_id":zone,"lat":lat,"lon":lon});
   print(node_id)

if __name__ == "__main__":
   main(sys.argv[1:])



