# This program should be executed in python 3

#!/usr/bin/python3

from cmd import Cmd
from shell_help import *
import subprocess, os, sys, shlex

MANUAL_NAME = "readme"
MAX_LINES_ON_SCREEN = 20

# get list containing lines of user manual file
manual_lines = build_file_list(MANUAL_NAME)

class MyShell(Cmd):

	def do_cd(self, args):
		"""Usage: cd [DIRECTORY]
   Change the current working directory to DIRECTORY. If DIRECTORY is not 
   supplied, the current working directory is reported."""

		args = args.split()

		# if no arguments present report current directory
		if len(args) == 0:
			print("Current working directory: " + os.getcwd())
		elif len(args) == 1:
			# try to change to new given directory if it exists
			try:
				cwd = os.getcwd()
				# change current working directory
				os.chdir(os.path.join(cwd, args[0]))
				# change PWD environment variable
				os.environ["PWD"] = os.getcwd()
				# prompt for user input with new current working directory
				self.prompt = os.getcwd() + ":~$ "
			# otherwise inform user about error encountered 
			except FileNotFoundError:
				print("cd: " + args[0] + ": No such file or directory")
			except NotADirectoryError:
				print("cd: " + args[0] + ": Not a directory")
			except PermissionError:
				print("Permission denied. Current user cannot access " + args[0])
		# otherwise inform user about error encountered
		elif len(args) > 1:
			print("Invalid 'cd' usage: too many arguments")

	def do_clr(self, args):
		"""Usage: clr
   Clear the terminal screen."""

		args = args.split()

		# if no arguments
		if len(args) == 0:
			# clear terminal screen via ascii ESCAPE value
			print("\033c", end = "")
		# otherwise inform user about correct usage of command
		else:
			print("Usage: clr")
			print("\nclr command takes no arguments.")
			
	def do_dir(self, args):
		"""Usage: dir [OPTION]... [FILE]...
   Display a list of files and subdirectories in FILEs (the current directory
   by default).
   Sort entries alphabetically if none of the options "-alr" are specified.

Options:
  -a, --all                  show hidden files too
  -l                         use a long listing format
  -r, --reverse              sort entries in reverse alphabetical order
  -R, --recursive            list subdirectories recursively"""

		args = args.split()

		if len(args) >= 2:
			# try output_redirection
			if output_redirection(["dir"] + args):
				# if redirection is not requested call command without redirection
				dir_no_redirect(args)
		else:
			# call command without redirection
			dir_no_redirect(args)

	def do_environ(self, args):
		"""Usage: environ
   List all the environment variables."""

		args = args.split()

		if len(args) == 0:
			# list all the environment variables
			for k, v in os.environ.items():
				print(k + "=" + v)
		# if only argument is a ampersand
		elif args[0] == "&":
			# run process without waiting for it to terminate
			subprocess.Popen(["env"], shell=False, stderr = subprocess.DEVNULL)
		elif len(args) >= 2:
			# try output_redirection
			if output_redirection(["env"] + args):
				# if output redirection not requested, inform user about correct usage of command
				print("Usage: environ")
				print("\nenviron command takes no arguments.")
		else:
			# inform user about correct usage of command
			print("Usage: environ")
			print("\nenviron command takes no arguments.")

	def do_echo(self, args):
		"""Usage: echo [ARG ...]
   Write arguments to the standard output.
    
   Display the ARGs, separated by a single space character and followed by a
   newline, on the standard output."""

		# split args into list without ignoring spaces entered between quotes
		try:
			args = list(shlex.shlex(args))
		# if spacing between quotes used incorrectly seperate all args by single space
		except ValueError:
			args = args.split()

		if len(args) >= 2:
			# try output_redirection
			if output_redirection(["echo"] + args):
				# if output redirection not requested, output arguments following command to screen
				print(" ".join(args))
		else:
			# output arguments following command to screen
			print(" ".join(args))

	def do_pause(self, args):
		"""Usage: pause
   Pause operation of the shell until "Enter" is pressed."""

		args = args.split()
		try:
			# if no arguments are given pause operation of the shell
			if len(args) == 0:
				# prompt for input until "Enter" is pressed
				inp = input("The operation of the shell has been temporarily paused, press 'Enter' to resume operations.\n")
			# otherwise inform user about usage of command
			else:
				print("Usage: pause")
				print("    pause command takes no arguments.")
		# deal with error case where user enters END OF TRANSMISSION character (ctrl + d)
		except EOFError:
			pass

	def do_help(self,args):
		"""Usage: help [CMD]
   List user manual with "help" or detailed information about individual 
   commands with 'help <CMD>'."""

		args = args.split()

		# if no arguments are given display the user manual
		if len(args) == 0:
			# initialize count of lines at 0
			count = 0
			# print one line at a time until MAX_LINES_ON_SCREEN is reached
			for line in manual_lines:
				print(line)
				count += 1
				# if MAX_LINES_ON_SCREEN is reached stop and prompt for input until <SPACEBAR> is entered
				if count == MAX_LINES_ON_SCREEN:
					inp = input("Press <SPACEBAR> followed by <ENTER> for more")
					#Erase last line outputted
					erase_previous_line()
					while inp != " ":
						inp = input("Press <SPACEBAR> followed by <ENTER> for more")
						#Erase last line outputted
						erase_previous_line()
					count = 0
		# if 3 or more arguments are given check if stdout redirection is requested
		elif len(args) >= 2:
			# check if command execution should run in background
			if args[-1] == "&":
				args = args[:-1]
			# try output redirection
			redirect_return_value = help_output_redirection(["help"] + args, manual_lines)
			# if requesting output redirection on specific command
			if redirect_return_value == -1:
				# get arguments
				other_args = " ".join(args[0:-2])
				redirect = args[-2]
				filename = args[-1]
				try:
					# get command help docstring
					help_line = MyShell.commands_help[other_args]
					# check if second last argument is stdout redirect symbol
					if redirect == ">":
						with open(filename, "w") as fout:
							fout.write(help_line)

					# check if second last argument is append stdout redirect symbol
					elif redirect == ">>":
						with open(filename, "a") as fout:
							fout.write("\n" + help_line)
				# if command does not exist inform user
				except KeyError:
					print("*** No help on " + other_args)

			# if output redirection not requested, use the default do_help method built_in the cmd module
			elif redirect_return_value == 1:
				Cmd.do_help(self, " ".join(args))
		# if output redirection not requested and arguments are given, use the default do_help method built_in the cmd module
		else:
			Cmd.do_help(self, " ".join(args))

	def do_quit(self, args):
		'''Usage: quit
   Exits the shell.'''

		args = args.split()

		# if no arguments
		if len(args) == 0:
			print ("\nExiting shell.")
			# exit shell
			raise SystemExit
		# otherwise inform user about correct usage of command
		else:
			print("Usage: quit")
			print("\nquit command takes no arguments.")

	# method that handles commands for which there is no do_xxx method (program invocation method)
	def default(self, args):
		'''Program invocation method.'''

		try:
			# if last command line argument is ampersand
			if args.split()[-1] == "&":
				# check if command is valid
				subprocess.check_output(args[:-1], shell = True, stderr = subprocess.STDOUT)
				# if so run process without waiting for it to terminate
				subprocess.Popen(args[:-1], shell=True, stderr = subprocess.DEVNULL)

			# otherwise launch program as child process and wait for it to terminate
			else:
				bytes_output = subprocess.check_output(args, shell = True, stderr = subprocess.STDOUT)
				# if no error encountered print generated by process
				print(bytes_to_string(bytes_output))

		# if command invalid, inform user
		except subprocess.CalledProcessError:
			print(args + ": command not found" )

	# Method called when an empty line is entered in response to the prompt. It is overridden to avoid repeating the last non-empty command entered as would be done by default
	def emptyline(self):
		pass

	# exits shell when user enters END OF TRANSMISSION character (ctrl + d)
	def do_EOF(self, args):
		'''Usage: EOF
   Exits the shell.'''
		self.do_quit(args)


	# dictionary used to output command (function) docstring when command called with help
	commands_help = {"cd" : do_cd.__doc__,
					"clr" : do_clr.__doc__,
					"dir" : do_dir.__doc__,
					"environ" : do_environ.__doc__,
					"echo" : do_echo.__doc__,
					"help" : do_help.__doc__,
					"pause" : do_pause.__doc__,
					"quit" : do_quit.__doc__,
					}

def main():
	args = sys.argv

	# set shell environment to path from which it was executed
	os.environ["SHELL"] = os.getcwd()
	# execute program without batchfile
	if len(args) == 1:
		prompt = MyShell()
		# prompt for user input with current working directory
		prompt.prompt = os.getcwd() + ":~$ "
		prompt.cmdloop('Starting prompt...')
	# execute program with batchfile
	elif len(args) == 2:
		batchfile = sys.argv[1]
		try:
			# readlines of batchfile into list
			with open(batchfile, "r") as fin:
				commands = []
				commands = fin.readlines()
			# quit shell when end of file is reached
			commands.append("quit")
			# execute one command at a time
			for command in commands:
				print(command, end = "")
				MyShell().onecmd(command.strip())
				print("\n")
		# inform user about error encountered
		except FileNotFoundError:
			print("bash: " + batchfile + ": No such file or directory")


if __name__ == '__main__':
	main()
