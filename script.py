#!/usr/bin/env python

'''
 ' A farmware for a custom tool for Farmbot
'''

import os, sys, json, Qualify
from random import randint
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

PIN_LIGHTS = 7
PKG = 'Test Bed'

input_errors = []
integer = Qualify.integer(PKG, 'integer')

tools = app.get_toolslots()
device.log(json.dumps(tools))

tool = Qualify.get_tool(4469)
devicxe.log(json.dumps(tool))

device.write_pin(PIN_LIGHTS, 0, 0)
