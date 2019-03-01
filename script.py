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
		device.log('Qualify Integer "{}": {}, {}'.format(name, data, PKG))
		return data
	except:
		input_errors.append('Must be integer for input: {}.'.format(name))

def qualify_sequence(seq_name):
	if len(''.join(seq_name.split())) > 0 and seq_name.lower() != 'none':
		try:
			sequence_id = app.find_sequence_by_name(name = seq_name)
			return sequence_id
		except:
			input_errors.append('Failed to find sequence ID for {}'.format(seq_name))
	return None

def chomp():
	for i in range(3):
		device.set_servo_angle(SERVO_PIN, SERVO_OPEN_ANGLE)
		device.wait(500)
		device.set_servo_angle(SERVO_PIN, SERVO_CLOSE_ANGLE)
		device.wait(500)

PIN_LIGHTS = 7
PKG = 'AudryII'

input_errors = []

SERVO_PIN = qualify_int('servo_pin')
SERVO_OPEN_ANGLE = qualify_int('servo_open_angle')
SERVO_CLOSE_ANGLE = qualify_int('servo_close_angle')
PLANT_TYPE = get_config_value(PKG, 'plant_type', str).lower()
Z_TRANSLATE = qualify_int('z_translate')
BED_HEIGHT = qualify_int('bed_height')
device.log('Plant Type: {}'.format(PLANT_TYPE))

audrey_retrieve_sequence_id = qualify_sequence(get_config_value(PKG, 'audrey_retrieve', str))
audrey_return_sequence_id = qualify_sequence(get_config_value(PKG, 'audrey_return', str))

if len(input_errors):
	for err in input_errors:
		device.log(err, 'error', ['toast'])
	sys.exit()
else:
	device.log('No config errors detected')

all_plants = app.get_plants()
target_plants = [];
for plant in all_plants:
	if plant['name'].lower() == PLANT_TYPE:
		target_plants.append(plant)

if not len(target_plants):
	device.log('No plants found with name: "{}"'.format(PLANT_TYPE))
	sys.exit()

device.log('Target Plants: {}'.format(json.dumps(target_plants)))
device.write_pin(PIN_LIGHTS, 1, 0)

device.execute(audrey_retrieve_sequence_id)
coord = Coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
coord.move_abs()
for site in target_plants:
	coord.set_coordinate(site['x'], site['y'], Z_TRANSLATE)
	coord.move_abs()
	coord.set_axis_position('z', BED_HEIGHT)
	coord.move_abs()
	chomp()
	coord.set_axis_position('z', Z_TRANSLATE)
	coord.move_abs()

device.execute(audrey_return_sequence_id)

device.write_pin(PIN_LIGHTS, 0, 0)
