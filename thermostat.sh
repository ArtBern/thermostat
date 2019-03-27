#!/bin/sh
mkdir -m 777 -p /var/run/mqtt2rrd
/opt/MQTT2RRD/mqtt2rrd.py start --config_file /opt/MQTT2RRD/mqtt2rrd.conf
cd /opt/thermostat
KIVY_BCM_DISPMANX_ID=2 python3 thermostat.py


