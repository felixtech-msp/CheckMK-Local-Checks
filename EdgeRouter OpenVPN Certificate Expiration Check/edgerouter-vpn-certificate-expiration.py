#!/usr/bin/env python3

# configuration parameters
ROUTER_IP='192.168.1.1'
ROUTER_USERNAME='ubnt'
ROUTER_KEYFILE='/usr/lib/check_mk_agent/local/edgerouter.key'
DAYS_WARNING=14
DAYS_CRITICAL=7

# do not change something below this line

import paramiko
import os
from datetime import datetime

def filter_string(str):
    return ''.join(c for c in str if c.isprintable())

def check_expiration(date):
    d = datetime.strptime(date, "%Y-%m-%d").date()
    now = datetime.now().date()
    return (d - now).days

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ROUTER_IP, username=ROUTER_USERNAME, key_filename=ROUTER_KEYFILE)

output = client.exec_command('find /config/auth/ -name "*.pem" -exec bash -c \'echo "$0>$(openssl x509 -enddate -noout -in "$0")"\' {} \;')[1]

list = []

for line in output:
    fileDateArray = line.split('>notAfter=')

    if '>' in fileDateArray[0]:
      continue

    if not fileDateArray[0]:
      continue

    list.append(fileDateArray)

for array in list:
    fileName = array[0].replace('/config/auth/','')
    longDate = filter_string(array[1])
    date = os.popen('date --date="' + longDate + '" --utc +"%Y-%m-%d"').read()
    date = filter_string(date)
    days = check_expiration(date)

    if days < DAYS_CRITICAL:
        print('2 "VPN Certificate \'' + fileName + '\'" - expires in ' + str(days) + ' days')
    elif days < DAYS_WARNING:
        print('1 "VPN Certificate \'' + fileName + '\'" - expires in ' + str(days) + ' days')
    else:
        print('0 "VPN Certificate \'' + fileName + '\'" - expires in ' + str(days) + ' days')

client.close()
