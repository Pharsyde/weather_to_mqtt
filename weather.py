#!/usr/bin/python
# -*- coding: utf-8 -*-
import paho.mqtt.publish as publish
import requests
import json
import logging

logging.basicConfig(format = u'%(filename)s [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG, filename = u'weather.log')
shops=[
  {'prefix': 'x508670', 'lat':55.638717, 'lng':37.358320},
  {'prefix': 'x506900', 'lat':55.806397, 'lng':37.614970}]
openweather_api='37994df6f8aba065bc6718ba31a6604a'
broker_address='91.238.227.244'
broker_port=1883
client_id='dbexport'
keep_alive_interval = 45
for shop in shops:
  try:
    url = 'http://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f&appid=%s' % (shop['lat'], shop['lng'], str(openweather_api))
    response = requests.get(url);
    data = json.loads(response.content)
  except:
    temp = -273
    logging.error(u'unable to fetch temeprature data: %s' % (e))
  else:
    temp = float(data['main']['temp'])-273.15
  try:
    topic_str = '%s/devices/out_weather/controls/Temperature' % (shop['prefix'])
    temp_str = '%.2f' % (temp)
    rc = publish.single(topic_str, temp_str, hostname=broker_address, port=broker_port, client_id=client_id, keepalive=int(keep_alive_interval))
    pass
  except Exception as e:
    logging.error(u'unable to publish to MQTT broker: %s' % (e))
  else:
  	logging.info(u'succesful publish: %s/%.2f.' % (shop['prefix'], temp))
