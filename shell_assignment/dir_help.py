# Student name: Stefano Puzzuoli
# Student number: 17744421

# This module is compatible with python 3

#!/usr/bin/python3

import subprocess, os

def dir_no_redirect(args):
	'''Input: arguments given to dir command
	Outputs: files and directories or error messages depending on arguments given'''

	if len(args) == 0:
		# print sorted files and directories of cwd
		for fn in sorted(os.listdir()):
			print(fn)
	elif len(args) == 1:
		try:
			# check if first argument is a command option
			first_char = args[0][0]
			if first_char == "-":
				try:
					# check if is long format output option
					if args[0] == "-l":
						dir_l(".")
					# check if is hidden files option
					elif args[0] == "-a" or args[0] == "--all":
						dir_a(".")
					# check if is reverse output option
					elif args[0] == "-r" or args[0] == "--reverse":
						dir_r(".")
					# if not call command as subprocess with arguments
					else:
						subprocess.call(["dir"] + args, stderr = subprocess.STDOUT)
				# if invalid command inform user about it
				except (IndexError, subprocess.CalledProcessError):
					print("dir: invalid option '" + args[0][1:] + "'")
					print("Try 'help dir' for more information.")
				# if invalid filename or option inform user about it
				except FileNotFoundError:
					print("dir: cannot access '" + args[0] + "': No such file or directory")
				except PermissionError:
					print("Permission denied. Current user cannot access " + args[0])

			# if only argument is a ampersand
			elif args[0] == "&":
				# run process without waiting for it to terminate
				subprocess.Popen(["dir"], stderr = subprocess.DEVNULL)
			else:
				try:
					# if only argument is filename print files and directories inside that file
					for fn in os.listdir(args[0]):
						print(fn)
				# if invalid filename inform user about it
				except FileNotFoundError:
					print("dir: cannot access '" + args[0] + "': No such file or directory")
		except NotADirectoryError:
			print(args[0] + " is not a directory.")

	else:
		subprocess.call(["dir"] + args)

# dir -r command function
def dir_r(filename):
	'''Input: filename
	Outputs: files and directories of filename in reverse order'''
	# print files and directories of cwd in reverse sorted order
	for fn in sorted(os.listdir())[::-1]:
		print(fn)

# dir -a command function
def dir_a(filename):
	'''Input: filename
	Outputs: files and directories of filename including hidden files'''
	dirs = os.listdir(filename)
	# add hidden files of cwd to directories that will be outputted
	dirs += [os.curdir, os.pardir]
	# print sorted files and directories of cwd (including hidden ones)
	for fn in sorted(dirs):
		print(fn)

# dir -l command function
def dir_l(filename):
	'''Input: filename
	Outputs: long listing format of file in well-aligned columns'''
	entries = []
	# iterate through each filename in directory
	for fn in os.listdir(filename):
		entries.append(long_entry(fn))

	# output info of file in long listing format
	print_long_entries(entries)

def print_long_entries(entries):
	'''Input: list of long listing format info of file
	Output: long listing format of file in well-aligned columns'''
	# get max widths of all columns
	column_widths = determine_columns_widths(entries)

	# print long listing format info of file aligning each columns depending on its max width
	for entry in entries:
		formatted_entry = " ".join([s.rjust(column_widths[i]) for i, s in enumerate(entry[:-1])] + [entry[-1]])
		print(formatted_entry)

def determine_columns_widths(entries):
	'''Input: list of long listing format info of file
	Returns: list containg max widths of each column for output'''
	column_widths = []
	for i in range(0, len(entries[0]) - 1):
		column = [row[i] for row in entries]
		column_widths.append(len(max(column, key = len)))
	return column_widths

def long_entry(fn):
	'''Input: filename
	Returns: long listing format of file as list'''

	# functions used to get user and group ids of files
	from pwd import getpwuid
	from grp import getgrgid

	# get all long listing info of file
	filestats = os.lstat(os.path.join(os.getcwd(), fn))

	# return long listing info in a list with each entry in desired format
	return [
		formatted_mode(filestats.st_mode),
		str(filestats.st_nlink),
		getpwuid(filestats.st_uid).pw_name,
		getgrgid(filestats.st_gid).gr_name,
		str(filestats.st_size),
		formatted_time(filestats.st_mtime),
		fn
		]

def formatted_time(st_mtime):
	'''Input: time as stat structure
	Returns: time as long listing format string'''
	import datetime
	# check if file from over a year ago
	dt = datetime.datetime.fromtimestamp(st_mtime)
	# if yes get year instead of time
	if dt < datetime.datetime.now() - datetime.timedelta(days = 365):
		return dr.strftime("%b %d  %Y")
	# otherwise get time instead of year
	return dt.strftime("%b %d %H:%M")

def formatted_mode(st_mode):
	'''Input: permissions as stat structure
	Returns: permissions as long listing format string'''
	# list of permission modes
	mode_chars = ["r", "w", "x"]
	# only consider last 9 chars which are ones that indicate permissions
	st_perms = bin(st_mode)[-9:]
	mode = filetype_char(st_mode)
	# add permissions that file has to permission long listing format string
	for i, perm in enumerate(st_perms):
		if perm == "0":
			mode += "-"
		else:
			mode += mode_chars[i % 3]
	return mode

def filetype_char(mode):
	'''Input: permissions as stat structure
	Returns: type of file'''
	import stat
	# return d for directory
	if stat.S_ISDIR(mode):
		return 'd'
	# return l for simlink
	if stat.S_ISLNK(mode):
		return 'l'
	# return - when neither
	return '-'
