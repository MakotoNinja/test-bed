#!/usr/bin/env python

from farmware_tools import device, app, get_config_value
PKG = 'Audrey II'

def combo(input_name):
	string = get_config_value(PKG, input_name, str)
	string = ''.join(input_name.split(' ')).lower()
	if ',' not in string:
		input_errors.append('Combo field does not contain a comma: {}'.format(input_name))
	else:
		split = string.split(',')
		if split[0] not in 'xy':
			input_errors.append('Left side of comma must be "X" or "Y". Found: {}'.format(split[0]))
			return None
		try:
			split[1] = int(split[1])
		except:
			input_errors.append('Right side of comma should be an Integer. Found: {}'.format(split[1]))
			return None
		return {'axis' : split[0], 'value' : split[1]}

def integer(input_name):
	data = get_config_value(PKG, input_name, int)
	try:
		data = int(data)
	except:
		input_errors.append('Must be integer for input: {}.'.format(input_name))
	else:
		return data

def sequence(input_name):
	seq_name = get_config_value(PKG, input_name, str)
	if ''.join(seq_name.split()).lower() == 'none':
		input_errors.append('Encountered "None" for required sequence {}" '.format(input_name))
		return False
	elif len(''.join(seq_name.split())) > 0:
		try:
			sequence_id = app.find_sequence_by_name(name = seq_name)
			return sequence_id
		except:
			input_errors.append('Failed to find sequence ID for {}'.format(seq_name))
	return None
