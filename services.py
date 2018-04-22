#!/usr/bin/env python

from __future__ import print_function

import sys
import time
import socket
import subprocess
from blinkstick import blinkstick

# Based on Internet connectivity status
# https://github.com/arvydas/blinkstick-python/wiki/Example%3A-Display-Internet-connectivity-status
#
# Checks a list of host/port, host ping or URI services
# Assigned LED pulses green for services online
# Assigned LED stays red for services offline


"""
Check the status of an online service
host and port are optional
uri is optional
"""
def status(v):
  description = v['description']
  connected   = v['connected']
  index       = v['index']
  online      = False

  if 'uri' in v:
    uri = v['uri']
    online = subprocess.Popen(['wget', '--connect-timeout', '2', '-t', '1', '-O', '-', uri], stdout = subprocess.PIPE, stderr = subprocess.PIPE).wait() == 0
  else:
    host = v['host']
    if 'port' in v:
      port = v['port']
      try:
        socket.setdefaulttimeout(2)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        online = True
      except Exception as ex:
        pass

    else:
      online = subprocess.Popen(['ping', '-c', '1', host], stdout = subprocess.PIPE, stderr = subprocess.PIPE).wait() == 0

  # Log status changes
  if online and connected != True:
      print('%s is online'%(description))

  if not online and connected != False:
      print('%s is offline'%(description))

  # Set LED colour
  if online:
    if connected == True:
      led.pulse(index=index, red=0, green=16, blue=0)
    else:
      led.morph(index=index, green=255)
  else:
    if connected == False:
      led.morph(index=index, red=16, green=0, blue=0)
    else:
      led.morph(index=index, red=255)

  return online

#####################################################

services = [
  { 'description': 'Google Australia', 'connected': None, 'host': 'google.com.au',  'port': 80, 'index': 0 },
  { 'description': 'Google USA',       'connected': None, 'host': 'google.com',     'port': 80, 'index': 1 },
  { 'description': 'Facebook',         'connected': None, 'host': 'facebook.com',   'port': 80, 'index': 2 },
  { 'description': 'Netflix',          'connected': None, 'host': 'netflix.com.au', 'port': 80, 'index': 3 },
  { 'description': 'Router',           'connected': None, 'host': '10.0.0.1',       'port': 53, 'index': 4 },
  { 'description': 'Linux2',           'connected': None, 'host': '10.0.0.4',                   'index': 5 },
  { 'description': 'Linux3',           'connected': None, 'host': '10.0.0.134',                 'index': 6 },
# { 'description': 'Laptop',           'connected': None, 'host': '10.0.0.13',                  'index': 7 },
  { 'description': 'Website',          'connected': None, 'uri': 'http://www.nigels.com/',      'index': 7 },
]

led = None

while True:

  if not led:
    while not led:
      print('Looking for BlinkStick...')
      try:
        led = blinkstick.find_first()
      except:
        led = None
      if not led:
        time.sleep(2)

  for s in services:
    s['connected'] = None
  for i in range(0,8):
      led.set_color(index=i, red=0, green=0, blue=0)

  try:
    while True:
      for s in services:
        s['connected'] = status(s)

  except KeyboardInterrupt:
    print('Ctrl-C Exit...')
    if led:
      for i in range(0,8):
          led.set_color(index=i, red=0, green=0, blue=0)
    sys.exit(0)

  except:
    led = None


