#!/usr/bin/env python

'''
 ' A farmware for a custom tool for Farmbot
'''

import os, sys, json, Qualify
from random import randint
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

def chomp():
	for i in range(3):
		device.set_servo_angle(SERVO_PIN, SERVO_OPEN_ANGLE)
		device.wait(500)
		device.set_servo_angle(SERVO_PIN, SERVO_CLOSE_ANGLE)
		device.wait(500)

PIN_LIGHTS = 7
PKG = 'Audrey II'

input_errors = []

SERVO_PIN = qualify_int('servo_pin')
SERVO_OPEN_ANGLE = qualify_int('servo_open_angle')
SERVO_CLOSE_ANGLE = qualify_int('servo_close_angle')
PLANT_TYPE = get_config_value(PKG, 'plant_type', str).lower()
Z_TRANSLATE = qualify_int('z_translate')
BED_HEIGHT = qualify_int('bed_height')
NUM_BITES = qualify_int('num_bites')
BITE_ADVANCE = qualify_int('bite_advance')
DUMP_OFFSET = qualify_combo('dump_offset')

if strip_str(DUMP_OFFSET).split()

audrey_retrieve_sequence_id = qualify_sequence('audrey_retrieve')
audrey_return_sequence_id = qualify_sequence('audrey_return')

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

device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
