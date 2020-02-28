import urllib.parse
from env import *
import sys, getopt
import xml.etree.ElementTree as ET
import re
import apiguifi
import sys,getopt
from env import *
import json

g=apiguifi.apiguifi(False)
g.login(username,password)
mod=g.send_request("guifi.misc.model",{"fid":"8"})
modj=json.loads(mod)
print(json.dumps(modj, indent=4, sort_keys=True))
