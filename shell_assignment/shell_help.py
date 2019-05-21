# Student name: Stefano Puzzuoli
# Student number: 17744421

# This module is compatible with python 3

#!/usr/bin/python3

import subprocess, os
from dir_help import *


def output_redirection(args):
	'''Redirect std output of command to a file.

	Argument args should have the following structure:
	[command, optional_args, redirect_symbol, output_filename].
	'''
	# get arguments
	command = args[0]
	other_args = args[1:-2]
	redirect = args[-2]
	filename = args[-1]
	try:
		# check if second last argument is stdout redirect symbol
		if redirect == ">":
			# if command valid get output of command in bytes otherwise throws error
			bytes_output = subprocess.check_output([command] + other_args, stderr = subprocess.DEVNULL)
			with open(filename, "w") as fout:
				# convert bytes to string and write to output file
				fout.write(bytes_to_string(bytes_output) + "\n")
			# return 0 to indicate that stdout redirection had occured
			return 0
		# check if second last argument is append stdout redirect symbol
		elif redirect == ">>":
			with open(filename, "a") as fout:
				# get output of command in bytes
				bytes_output = subprocess.check_output([command] + other_args, stderr = subprocess.DEVNULL)
				# convert bytes to string and append to output file
				fout.write("\n" + bytes_to_string(bytes_output))
			# return 0 to indicate that stdout redirection had occured
			return 0
		# if second last argument is not stdout redirect symbol call command without redirection
		else:
			# if last command line argument is ampersand
			if args[-1] == "&":
				subprocess.check_output(args[:-1], shell = True, stderr = subprocess.STDOUT)
				# if so run process without waiting for it to terminate
				subprocess.Popen(" ".join(args[:-1]), shell = True, stderr = subprocess.DEVNULL)
				return 0
			else:
				# return 1 to indicate that stdout redirection has not occured
				return 1
	except subprocess.CalledProcessError:
		print("Invalid use of " + command + ". Try 'help " + command + "' for more information")
	except PermissionError:
		print("Permission denied. Current user cannot write to " + filename)


def help_output_redirection(args, manual_lines):
	'''Redirect std output of help command to a file.

	Argument args should have the following structure:
	[command, redirect_symbol, output_filename].
	'''
	# get arguments
	command = args[0]
	other_args = args[1:-2]
	redirect = args[-2]
	filename = args[-1]
	try:
		if len(other_args) == 0:
			# check if second last argument is stdout redirect symbol
			if redirect == ">":
				with open(filename, "w") as fout:
					for line in manual_lines:
						fout.write(line + "\n")
				# return 0 to indicate that stdout redirection had occured
				return 0
			# check if second last argument is append stdout redirect symbol
			elif redirect == ">>":
				with open(filename, "a") as fout:
					# output new line before appending text
					fout.write("\n")
					for line in manual_lines:
						fout.write(line + "\n")
				# return 0 to indicate that stdout redirection had occured
				return 0
			# if second last argument is not stdout redirect symbol call command without redirection
			else:
				# return 1 to indicate that stdout redirection has not occured
				return 1

		# return -1 to indicate case of requesting output redirection on individual command
		else:
			return -1
	except subprocess.CalledProcessError:
		print("Invalid use of " + command + ". Try 'help " + command + "' for more information")
	except PermissionError:
		print("Permission denied. Current user cannot write to " + filename)


def build_file_list(filename):
	'''Returns list containing all lines of a file.'''
	lines = []
	# append lines of file into list
	with open(filename, "r") as fin:
		for line in fin:
			lines.append(line.rstrip())
	return lines


def bytes_to_string(bytes):
	'''Returns string obtained from conversion of inputted bytes'''
	return "".join(map(chr, bytes)).strip()


def erase_previous_line():
	'''Erases last line outputted on STDOUT'''
	#use VT100 cursor control codes to delete "Press <Enter> for more" line after Enter is pressed
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'
	print(CURSOR_UP_ONE + ERASE_LINE, end = "")

