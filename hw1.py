import csv
import sys
import math
import imp
import os

def read_data(file_name):
    return list(csv.reader(open(file_name, 'rt')))

def create_dictionary(data, output):
	dict = {}
	for index_row, row in enumerate(data):
		for index_column, cell in enumerate(row):
			if cell[0] != '=':
				dict[chr(ord('A') + index_column) + str(index_row + 1)] = cell
	return dict

def change_for_func(commands_list, module_name, cell):
	new_cell = cell
	for command in commands_list:
		new_cell = new_cell.replace(command + '(', module_name + command + '(')
	return new_cell


def calculate(dict, output):
	for index_row, row in enumerate(data):
		for index_column, cell in enumerate(row):
			if cell[0] == '=':
				cell = change_for_func(math_commands, 'math.', cell)
				cell = change_for_func(module_commands, "module.", cell)
				cell = cell[1:]
				for known_cell, item in dict.items():
					if item.isdigit() or item.replace('.', '' ,1).isdigit():
						cell = cell.replace(known_cell, item)
					else:
						cell = cell.replace(known_cell, '\"' + item + '\"')
				try:
					output[index_row][index_column] = eval(cell)
				except Exception as exc:
					output[index_row][index_column] = "ERROR"


def write_data(output_name, output_table):
	c = csv.writer(open(output_name, "w"))
	for row in output_table:
		c.writerow(row)


def module_preparation():
	module_commands = []
	for command in dir(module):
		if command[0] != '_':
			module_commands.append(command)
	return module_commands

data = read_data(sys.argv[1])

if (len(sys.argv) > 3):
	module_name = sys.argv[3]
	module = imp.load_source(module_name, os.getcwd() + '/' + module_name)
	module_commands = module_preparation()
else:
	module_commands = []

output = data

dict = create_dictionary(data, output)

math_commands = dir(math)
calculate(dict, output)
write_data(sys.argv[2], output)

