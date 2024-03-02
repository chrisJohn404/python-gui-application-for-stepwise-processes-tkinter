'''
Python GUI Application for Stepwise Processies, as vanilla python as possible.
Author: Chris Johnson (chrisjohn404)
September 2020
License: GPLv2
 - Starting point for running application.  Handles CLI options and logic
   necessary for running as an application vs python script.xample application
   for running stepwise processies, pure python.
'''

import sys
import os
from os import path
import inspect
import tempfile
import importlib
import importlib.util
import argparse
import traceback
import atexit
import argparse
from pathlib import Path

# Import shared library files.

# Enable imports among files in the tp_core path fixing issue in python 3.11
sys.path.insert(0, path.join(Path(__file__).resolve().parent,'tp_core'))

import tp_core.gui
from tp_core.gui import TestApplicationInit
from tp_core.cli_gui import CliTestApplication

# Determine if running as app or python process.
isExecAsPyProc = True
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
	isExecAsPyProc = False

# Define default exit handler
c_exit_handler = None
def def_exit_handler():
	if c_exit_handler:
		c_exit_handler()
	return
atexit.register(def_exit_handler)

# Define a function that gets called to enable processie sets
# to run code on exit.
def registerExitHandler(exitHandler):
	c_exit_handler = exitHandler

# Define Application Runner
def runApp(isGui, numExec, process=''):
	print('in runApp', isGui, numExec, process)
	'''
	Function that runs application.

	@isGui: Boolean GUI/CLI
	@process: String path file to load.
	'''
	initializedTestManager = False

	if process=='':
		# Import process
		try:
			from def_tests import TestManager
		except:
			print('TestManager should be defined and follow "UpperCamel" Case')
			from def_tests import testManager

		# Initialize the overall test manager that
		# performs set-up & tear down routines and
		# contains a list of all of the process
		try:
			initializedTestManager = TestManager()
		except:
			print('TestManager should be defined and follow "UpperCamel" Case')
			initializedTestManager = testManager()
	else:
		# Split the path {dir, file} of the user specified test file.
		splitPath = path.split(process)
		fDir = splitPath[0]
		fName = splitPath[1]

		# Add current file's directory to import path.
		sys.path.insert(0, fDir)

		if isExecAsPyProc:
			# Add current file's directory + 'tp_core' to import path.
			sys.path.insert(0, path.join(path.dirname(path.abspath(__file__)),'tp_core'))
		else:
			# Add executable file's directory to import path.
			sys.path.insert(0, path.split(sys.executable)[0])

		try:
			testManager = importfile(
				path.join(fDir,fName), 'TestManager').TestManager #REF DOWN.
		except:
			print('TestManager should be defined and follow "UpperCamel" Case')
			testManager = importfile(
				path.join(fDir,fName), 'testManager').testManager #REF DOWN.
		
		initializedTestManager = testManager()
		
	if isGui:
		# Start GUI APP
		app = TestApplicationInit(initializedTestManager)
	else:
		# Execute as CLI App
		testApp = CliTestApplication(initializedTestManager)
		testApp.startTest()

# Customized import function
def importfile(file_path, class_name):
	'''
	Function which enables custom loading of python module.

	@file_path: String: Path to *.py to load.
	@class_name: String: Name of class to import.
	'''
	spec = importlib.util.spec_from_file_location(class_name, file_path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[class_name] = module
	m = spec.loader.exec_module(module)
	return module

example_text='''
Example:
`python3 main.py ./example_tests/tests.py`
`python3 main.py -r ./example_tests/tests.py`

Run in CLI mode:
`python3 main.py -c -r ./example_tests/tests.py`
'''

# If this is the main application, then run...
if __name__ == "__main__":
	def printHelp():
		print('Stepwise Processies Application (Help Menu)')
		parser.print_help()
		print(example_text)

	execApp = True
	execGui = True
	numExec = -1

	# Read system environment variables to alter default state.
	if os.environ.get('PGAFSPT_EXEC_GUI') is not None:
		execGui = os.environ.get('PGAFSPT_NUM_EXEC')
	if os.environ.get('PGAFSPT_EXEC_GUI') is not None:
		execGui = os.environ.get('PGAFSPT_NUM_EXEC')
	
	# localTestLibs = False # Conditionally allow user script to import files, was exposed w/ "-l"
	processies = []

	parser = argparse.ArgumentParser(
		description='Pass a file "path" that defines a set of stepwise processies.'
	)
	parser.version = '0.1.0'
	parser.add_argument('processies', metavar='path', type=str, nargs='?', default='', help='Path of file to run.')
	parser.add_argument('-c','--cli', action='store_false', help='Run in CLI mode.', dest='exec_gui')
	parser.add_argument('-n','--num-executions', action='store', type=int, default=-1, metavar='N', help='Run processie [n] number of times.', dest='num_exec')
	parser.add_argument('-r','--run-file', action='store', type=str, metavar='path', help='Run file path.', dest='run_file')

	args = parser.parse_args()
	# print(vars(args))
	execGui = args.exec_gui
	numExec = args.num_exec

	if args.run_file:
		processies.append(args.run_file)
	else:
		if isinstance(args.processies, list):
			if len(args.processies) > 0:
				processies.append(args.processies[0])
		elif args.processies != '':
			processies.append(args.processies)
	try:
		'''
		if len(sys.argv) > 1:
			ci=1
			if isExecAsPyProc:
				ci=1
			while ci < len(sys.argv):
				arg=sys.argv[ci]
				if arg == '-c' or arg == '--cli':
					execGui = False; ci+=1; continue
				if arg == '-n' or arg == '--num-executions':
					numExec = int(sys.argv[i+1]); ci+=2; continue
				if arg == '-r' or arg == '--run-file':
					processies = path.realpath(sys.argv[i+1]); ci+=2; continue
				if arg == '-h' or arg == '--help':
					execApp = False; ci+=1; continue
				processies.append(arg)
				ci+=1
		'''

		if execApp and len(processies) > 0:
			runApp(execGui, numExec, process=processies[0])
		elif execApp:
			runApp(execGui, numExec)
		else:
			# printHelp()
			parser.print_help()
	except Exception as err:
		arg_str = ' '.join(sys.argv)
		print(f'Encountered an error running: {sys.executable} {arg_str}')
		traceback.print_exc()
		print('---------------------------------------------------------------')
		printHelp()
		# parser.print_help()












''' Author(s): Chris Johnson (chrisjohn404) '''