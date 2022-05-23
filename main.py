'''
Python GUI Application for Stepwise Processies, as vanilla python as possible.
Author: Chris Johnson (chrisjohn404)
Circa 2020
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

# Import shared library files.
import tp_core.gui
from tp_core.gui import TestApplicationInit
from tp_core.cli_gui import CliTestApplication

# Determine if running as app or python process.
isExecAsPyProc = True
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    isExecAsPyProc = False


# Define Application Runner
def runApp(isGui, process=''):
    '''
    Function that runs application.

    @isGui: Boolean GUI/CLI
    @process: String path file to load.
    '''
    initializedTestManager = False

    if process=='':
        # Import process
        from def_tests import testManager

        # Initialize the overall test manager that
        # performs set-up & tear down routines and
        # contains a list of all of the process
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

def printHelp():
    print('''Stepwise Processies Application (Help Menu)
    Usage: main.py [-h] [-c] process_path

    Pass a file containing tests.

    Options:
    -c, --cli         Run in CLI mode.
    -r, --run-file    Run a specified "[user_]tests.py" file.
          Ex: [app] -r ./user_tests/curl_tests.py

    -h, --help        Print help menu.

    Example:
    `python3 main.py ./example_tests/tests.py`
    ''')
# If this is the main application, then run...
if __name__ == "__main__":
    try:
        execApp = True
        execGui = True
        # localTestLibs = False # Conditionally allow user script to import files, was exposed w/ "-l"
        processies = []

        if len(sys.argv) > 1:
            ci=1
            if isExecAsPyProc:
                ci=1
            while ci < len(sys.argv):
                arg=sys.argv[ci]
                if arg == '-c' or arg == '--cli':
                    execGui = False; ci+=1; continue
                if arg == '-r' or arg == '--run-file':
                    processies = path.realpath(sys.argv[i+1]); ci+=2; continue
                if arg == '-h' or arg == '--help':
                    execApp = False; ci+=1; continue
                processies.append(arg)
                ci+=1

        if execApp and len(processies) > 0:
            runApp(execGui, process=processies[0])
        elif execApp:
            runApp(execGui)
        else:
            printHelp()
    except Exception as err:
        traceback.print_exc()
        print('---------------------------------------------------------------')
        printHelp()












''' Author(s): Chris Johnson (chrisjohn404) '''
