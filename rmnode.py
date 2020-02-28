#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import apiguifi
import sys,getopt
from env import *


def main(argv):
   node_name=""
   test = False
   node_id = ""
   def help():
      print('Usage: rmnode.py -h -t -n node_id')
      print('Removes node and all exising links and devices from this node.')
      print('	-h, --help		Display help and exit')
      print('	-t, --test		Use test.guifi.net instead of production website')
      print('	-n, --node_id		ID of the node to remove')
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
      elif opt in ("-n", "--node_id"):
         node_id = arg
   if node_id == "":
      print("Missing parameter node_id")
      help()
      sys.exit(2)

   g=apiguifi.apiguifi(test)
   g.login(username,password)
   g.remove_node(node_id);
   print("Node "+node_id+" removed succesfully")

if __name__ == "__main__":
   main(sys.argv[1:])



