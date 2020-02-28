#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import apiguifi
import yaml
from jinja2 import Environment, FileSystemLoader
import sys,getopt
from env import *
import os

def main(argv):
   node_id=""
   test = False
   template = ""
   pptp_user = "pptpuser"
   pptp_password = "pptppass"
   path=""
   filename=""

   def help():
      print('Usage: getvarfile.py -h -t -n node_id -j template_path [ -u pptp_user -p pptp_password ]')
      print('Gets the variables of the passed node and renders them in a template. Then, prints the resulting template.')
      print('	-h, --help		Display help and exit')
      print('	-t, --test		Use test.guifi.net instead of production website')
      print('	-n, --node_id		ID of the node')
      print('	-j, --template		Jinja2 template to write the variables')
      print('	-u, --pptp_user		PPTP username (optional)')
      print('	-p, --pptp_password	PPTP user password')
   try:
      opts, args = getopt.getopt(argv,"htn:j:u:p:",["node_id=","template="])
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
         node_id = arg
      elif opt in ("-u", "--pptp_user"):
         pptp_user = arg
      elif opt in ("-p", "--pptp_password"):
         pptp_password = arg
      elif opt in ("-j", "--template"):
         path, filename = os.path.split(arg)
         path = path or './' 

   if path == "" or node_id == "":
      print("Missing parameters")
      help()
      sys.exit(2)

   g=apiguifi.apiguifi(test)
   tpl = Environment(loader=FileSystemLoader(path)).get_template(filename)
   node = g.get_node_data(node_id)
   if node['dev_model'] == "Routerboard SXT Lite5":
      main_wlan="wlan2"
   else:
      main_wlan="wlan1"

   print(tpl.render(main_wlan=main_wlan,pptp_username=pptp_user,pptp_password=pptp_password,ssid=node['dev_ssid'],location=node['dev_location'],dev_hostname=node['dev_title'],node_id=node_id,dev_ip=node['dev_ip'],dev_mask=node['dev_mask'],dev_gw=node['dev_gateway']))

if __name__ == "__main__":
   main(sys.argv[1:])



