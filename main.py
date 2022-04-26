'''
Example application for running stepwise processies, pure python.
Author(s): Chris Johnson
September 2019


'''
import sys
import os
from os import path
import inspect
import tempfile
import importlib
import importlib.util

# Import shared library files.
import tp_core.gui
from tp_core.gui import TestApplicationInit
from tp_core.cli_gui import CliTestApplication

# Determine if running as app or python process.
isExecAsPyProc = True
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    isExecAsPyProc = False

# Customized import function
def importfile(file_path, class_name):
	spec = importlib.util.spec_from_file_location(class_name, file_path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[class_name] = module
	m = spec.loader.exec_module(module)
	return module

# define application runner
def runApp(isGui, tests=''):
	initializedTestManager = False

	if tests=='':
		# Import tests
		from def_tests import testManager

		# Initialize the overall test manager that
		# performs set-up & tear down routines and
		# contains a list of all of the tests
		initializedTestManager = testManager()
	else:
		# Split the path {dir, file} of the user specified test file.
		splitPath = path.split(tests)

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

		testManager = importfile(path.join(fDir,fName), 'testManager').testManager
		
		initializedTestManager = testManager()
		
	if isGui:
		# Start GUI APP
		app = TestApplicationInit(initializedTestManager)
	else:
		# Execute as CLI App
		testApp = CliTestApplication(initializedTestManager)
		testApp.startTest()

# If this is the main application, then run...
if __name__ == "__main__":
	execApp = True
	execGui = True
	# localTestLibs = False # Conditionally allow user script to import files, was exposed w/ "-l"
	tests = ''
	if len(sys.argv) > 1:
		for i, arg in enumerate(sys.argv):
			if arg == '-c' or arg == '--cli':
				execGui = False
			if arg == '-r' or arg == '--run-file':
				tests = path.realpath(sys.argv[i+1])
			if arg == '-h' or arg == '--help':
				execApp = False

	if execApp:
		runApp(execGui, tests=tests)
	else:
		print('Hello stepwise processies application')
		print('')
		print('-c, --cli         Run in CLI mode.')
		print('-r, --run-file    Run a specified "[user_]tests.py" file.')
		print('      Ex: [app] -r ./user_tests/curl_tests.py')
		print('')
		print('')
		print('-h, --help        Print help menu.')


