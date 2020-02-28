#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import apiguifi
import sys,getopt
from env import *


def main(argv):
   node_id=""
   test = False
   def help():
      print('Usage: scannode.py -h -t -n node_id')
      print('Scans AP near the node identified by node_id')
      print('	-h, --help		Display help and exit')
      print('	-t, --test		Use test.guifi.net instead of production website')
      print('	-n, --node NODE_ID	Node to scan nearby APs')
   try:
      opts, args = getopt.getopt(argv,"htn:",["node="])
   except getopt.GetoptError:
      help()
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         help()
         sys.exit()
      elif opt in ("-n", "--node"):
         node_id = arg
      elif opt in ("-t", "--test"):
         test = True
   if node_id == "":
      print("Missing parameter node_id")
      help()
      sys.exit(2)

   print('Scanning node '+  node_id+"...")
   g=apiguifi.apiguifi(test)
   g.login(username,password)
   g.print_near_aps(node_id)


if __name__ == "__main__":
   main(sys.argv[1:])

