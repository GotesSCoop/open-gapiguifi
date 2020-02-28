#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import urllib.parse
from env import *
import sys, getopt
import xml.etree.ElementTree as ET
import re


class apiguifi:

  Base_URL = "" # Base Guifi URL
  Base_auth_URL = "" # Base Guifi URL
  Base_CNML_URL = ""
  Base_OneClick_URL = ""
  Verify = "" # Check certificate (not in test case)
  authToken = ""

  DEFAULT_ZONE = 41583 # Sóller

  def login(self, user, password):
    # user: guifi.net web username
    # pasword: guifi.net web users password
    ret = self.send_request("guifi.auth.login",{"username":user,"password":password})
    dict_ret = json.loads(ret)
    self.authToken = dict_ret['responses']['authToken']

  def add_node(self, node_data):
    # node_data structure       Estructura amb les dades del node. Poden ser les següents (* = MANDATORY):
        # * title string  Nom del lloc del node guifi.net.        
        # nick  string  Nom curt del lloc.      generat automàticament
        # body  string  Descripció del node guifi.net.  generat automàticament
        # * zone_id       integer ID de zona on està ubicat aquest lloc.  
        # zone_description      string  Descripció de la zona on està localitzat el nou node guifi.net. 
        # notification  string  Adreça electrònica de notificació de canvis del node.   Adreça electrònica de l'usuari autenticat.
        # * lat   float   Latitud, en graus decimals, de la localització del node guifi.net.      
        # * lon   float   Longitud, en graus decimals, de la localització del node guifi.net.     
        # elevation     integer Elevació, en metres, de la localització del nou node guifi.net. 
        # stable        string  Serveix el node per expandir la xarxa? Possibles valors: Yes (Sí), No (No).     Yes
        # graph_server  integer ID del servidor de gràfiques que recull les dades de disponibilitat del dispositiu.     Agafat de la zona pare
        # status        string  Estat del dispositiu. Possibles valors: Planned (Projectat), Reserved (Reservat), Building (En construcció), Testing (En proves), Working (Operatiu) i Dropped (Esborrat).


    # RETORNA: Id del node
    ret = self.send_request("guifi.node.add",node_data)
    dict_ret = json.loads(ret)
    return dict_ret['responses']['node_id']

  def update_node(self, node_data):
    # node_data	structure	Estructura amb les dades del node. Poden ser les següents:
        # * node_id integer Id del node a actualitzar.
        # title	string	Nom del lloc del node guifi.net.	
        # nick	string	Nom curt del lloc.	generat automàticament
        # body	string	Descripció del node guifi.net.	generat automàticament
        # zone_id	integer	ID de zona on està ubicat aquest lloc.	
        # zone_description	string	Descripció de la zona on està localitzat el nou node guifi.net.	
        # notification	string	Adreça electrònica de notificació de canvis del node.	Adreça electrònica de l'usuari autenticat.
        # lat	float	Latitud, en graus decimals, de la localització del node guifi.net.	
        # lon	float	Longitud, en graus decimals, de la localització del node guifi.net.	
        # elevation	integer	Elevació, en metres, de la localització del nou node guifi.net.	
        # stable	string	Serveix el node per expandir la xarxa? Possibles valors: Yes (Sí), No (No).	Yes
        # graph_server	integer	ID del servidor de gràfiques que recull les dades de disponibilitat del dispositiu.	Agafat de la zona pare
        # status 	string	Estat del dispositiu. Possibles valors: Planned (Projectat), Reserved (Reservat), Building (En construcció), Testing (En proves), Working (Operatiu) i Dropped (Esborrat).

    ret = self.send_request("guifi.node.update",node_data)
    return ret

    


  def remove_node(self, node_id):
    # * node_id	integer	Id del node a esborrar
    ret = self.send_request("guifi.node.remove",{"node_id":node_id})
    return ret

  def get_near_ap(self, node_id):
    # Cerca els aps més propers al node passat
    # * node_id	integer	Id del node a cercar
    ret = self.send_request("guifi.radio.nearest",{"node_id":node_id})
    dict_ret = json.loads(ret)
    client_radios=[]
    for radio in dict_ret['responses']['radios']:
       if radio["ssid"].lower().find("clients") > -1:
          client_radios.append(radio)
    
    #return json.dumps(client_radios, indent=4, sort_keys=True)
    return client_radios

  def add_device(self, dev_data):
    # Afegeix un dispositiu al node passat
    # dev_data	structure	Estructura amb les dades del dispositiu. Consultau https://guifi.net/sites/all/modules/guifi/contrib/api_doc/index.php
    ret = self.send_request("guifi.device.add",dev_data)
    dict_ret = json.loads(ret)
    return dict_ret['responses']['device_id']

  def update_device(self, dev_data):
    # Afegeix un dispositiu al node passat
    # dev_data	structure	Estructura amb les dades del dispositiu. Consultau https://guifi.net/sites/all/modules/guifi/contrib/api_doc/index.php
    ret = self.send_request("guifi.device.update",dev_data)
    return ret

  def remove_device(self, dev_id):
    # Afegeix un dispositiu al node passat
    # dev_data  structure       Estructura amb les dades del dispositiu. Consultau https://guifi.net/sites/all/modules/guifi/contrib/api_doc/index.php
    ret = self.send_request("guifi.device.remove",{"dev_id":dev_id})
    return ret

  def add_radio(self, radio_data):
    # Afegeix una radio a un dispositiu
    # radio_data	structure	Estructura amb les dades de la radio.
    ret = self.send_request("guifi.radio.add",radio_data)
    dict_ret = json.loads(ret)
    return dict_ret['responses']['radiodev_counter']

  def update_radio(self, radio_data):
    # Actualitza una radio
    # radio_data	structure	Estructura amb les dades de la radio.
    ret = self.send_request("guifi.radio.update",radio_data)
    return ret
    
  def remove_radio(self, device_id, radiodev_counter):
    # Suprimeix una radio a un dispositiu
    # device_id	structure	Id del dispositiu
    # radidev_counter structure	Posicio de la radio dins del dispositiu
    ret = self.send_request("guifi.radio.remove", {"device_id":device_id, "radiodev_counter":radiodev_counter})
    return ret

  def add_link_to_AP(self, from_device_id, to_device_id, counter_from=0, counter_to=0):
    # Enllaça una radio a un AP
    # from_device_id: dispositiu origen
    # to_device_id: dispositiu desti
    # counter_from: posicio de la radio a l'origen. Opcional. Per defecte el primer.
    # counter_to: posicio de la radio al desti. Opcional. Per defecte el primer.
    ret = self.send_request("guifi.link.add", {"from_device_id":from_device_id,"from_radiodev_counter":counter_from,"to_device_id":to_device_id,"to_radiodev_counter":counter_to,"status":"Working"})

    dict_ret = json.loads(ret)
    return dict_ret['responses']

  def remove_link_to_AP(self, link_id):
    # Elimina un enllaç d'una radio a un AP
    ret = self.send_request("guifi.link.remove",{"link_id":link_id})
    return ret

  def get_node_data(self, node_id):
    ret = {}
    xmlret=self.get_cnml(node_id)
    root = ET.fromstring(xmlret)  

    try:
       node = root.find('node')
       ret['node_name'] = node.get('title')
       ret['node_status'] = node.get('status')
       ret['node_lat'] = node.get('lat')
       ret['node_lon'] = node.get('lon')
    except:
       pass 
    
    try:
       dev = node.find('device')
       ret['dev_id'] = dev.get('id')
       ret['dev_title'] = dev.get('title')
       ret['dev_status'] = dev.get('status')
       ret['dev_firmware'] = dev.get('firmware')
       ret['dev_model'] = dev.get('name')
    except:
       pass
   
    try:
       interf = dev.find('interface')
       ret['dev_ip'] = interf.get('ipv4')
       ret['dev_mask'] = interf.get('mask')
    except:
       pass

    try:
        if ret['dev_firmware'].lower().find("routeros") > -1 :
           oneclick = self.get_oneclick(dev.attrib['id']) # Alguns camps com l'SSID no apareixen correctament al CNML
           ret['dev_ssid'] = oneclick[oneclick.find('mode=station ssid="')+19:oneclick.find('band=""')-15]
           ret['dev_location'] = oneclick[oneclick.find('enabled=yes location="')+22:oneclick.find('" trap-community=public')]
           gateway_str=re.split("route add gateway=",oneclick)[1]
           ret['dev_gateway']=re.split("<br />",gateway_str)[0][:-1]
 
    except Exception as e:
        print(e.message)
        print("Not a RouterOS device")
        
        pass

    return ret

  def get_oneclick(self, node_id):
    get_url=self.Base_OneClick_URL+node_id+"/view/unsolclic"
    r = requests.get(get_url, verify = self.Verify)
    if r.status_code == 200:
      return r.text
    else:
      print("Error in One Click request")
      raise ValueError

  def get_cnml(self, node_id):
    get_url=self.Base_CNML_URL+node_id+"/node"
    r = requests.get(get_url, verify = self.Verify)
    if r.status_code == 200:
      return r.text
    else:
      print("Error in CNML request")
      raise ValueError


  def send_request(self, command, parameters):
    # Command: command to execute into guifi api
    # Parameters: dictionary of parameters
    params=urllib.parse.urlencode(parameters)
    get_url=self.Base_URL+command+"&"+params
    if self.authToken == "":
       r = requests.get(get_url, verify = self.Verify)
    else:
       authtok='GuifiLogin auth=' + self.authToken
       head = {'Authorization': authtok.encode('utf-8')}
       r = requests.get(get_url, verify = self.Verify, headers=head)

    if r.status_code == 200:
      return r.text
    else:
      print("Error in request")
      raise ValueError
    


  def __init__(self, test=True):

    if test == True :
      self.Base_URL = "http://test.guifi.net/api?command="
      self.Base_auth_URL = "http://test.guifi.net/api/auth?command="
      self.Base_CNML_URL = "http://test.guifi.net/guifi/cnml/"
      self.Base_OneClick_URL = "http://test.guifi.net/guifi/device/"
      Verify = False
    else:
      self.Base_URL="https://guifi.net/api?command="  
      self.Base_auth_URL="https://guifi.net/api/auth?command="  
      self.Base_CNML_URL = "https://guifi.net/guifi/cnml/"
      self.Base_OneClick_URL = "https://guifi.net/guifi/device/"
      Verify = True
    



  def print_near_aps(self, node_id):
     near_aps = self.get_near_ap(node_id)
     for i in near_aps:
        print("Device "+i['device_id'])
        print("   SSID: "+i['ssid'])
        print("   Distance: "+str(i['distance']))
        print("--- ")

    



#g=apiguifi(test=True)
#g.login(username,password)


#ap_id="nu"
#add_node(nom=NODE_NAME,lat=39.780969,lon=2.725782,ap_id=)

## Usage example:
#node_id=g.add_node({"title":NODE_NAME,"zone_id":41583,"lat":39.780969,"lon":2.725782});
#node_id=96168
#print g.get_near_ap(node_id)
#device_id = g.add_device({"model_id":70, "firmware":"RouterOSv6.x","nick":NODE_NAME+"_SXT5","mac":"00:00:00:00:00:00","node_id":node_id,"type":"radio"})
#radiodev_counter = g.add_radio({"mode":"client","device_id":device_id,"mac":"00:00:00:00:00:00","antenna_gain":14})
#print g.add_link_to_AP(device_id,91697,radiodev_counter,0)
#g.add_link_to_ap(from_device_id=)


