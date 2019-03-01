#!/usr/bin/env python

'''
 ' A farmware for a custom tool for Farmbot
'''

import os, sys, json
from random import randint
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

input_errors = []
def qualify_int(name):
	data = get_config_value(PKG, name, int)
	try:
		data = int(data)
	except:
		input_errors.append('Must be integer for input: {}.'.format(name))
	else:
		return data

def qualify_sequence(seq_name):
	if len(''.join(seq_name.split())) > 0 and seq_name.lower() != 'none':
		try:
			sequence_id = app.find_sequence_by_name(name = seq_name)
			return sequence_id
		except:
			input_errors.append('Failed to find sequence ID for {}'.format(seq_name))
	return None

PIN_LIGHTS = 7
PKG = 'AudryII'

input_errors = []


SERVO_PIN = qualify_int('servo_pin')

'''
water_tool_retrieve_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_water_retrieve', str)) #optional
water_tool_return_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_water_return', str)) #optional
weeder_tool_retrieve_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_weed_retrieve', str))
weeder_tool_return_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_weed_return', str))
'''

if len(input_errors):
	for err in input_errors:
		device.log(err, 'error', ['toast'])
	sys.exit()
else:
	device.log('No config errors detected')

device.write_pin(PIN_LIGHTS, 1, 0)

plants = app.get_plants()
device.log('Plants: {}'.format(json.dumps(plantts)))

device.write_pin(PIN_LIGHTS, 0, 0)
