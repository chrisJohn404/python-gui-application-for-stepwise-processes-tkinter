'''
Example application for running stepwise processies, pure python.
Author(s): Chris Johnson
September 2019


'''
import sys

# Import shared library files.
import tp_core.gui
from tp_core.gui import TestApplicationInit
from tp_core.cli_gui import CliTestApplication

# Import tests
from tests import testManager


def runApp(isGui):
	# Initialize the overall test manager that
	# performs set-up & tear down routines and
	# contains a list of all of the tests
	initializedTestManager = testManager()

	if isGui:
		# Start GUI APP
		app = TestApplicationInit(initializedTestManager)
	else:
		# Execute as CLI App
		testApp = CliTestApplication(initializedTestManager)
		testApp.startTest()


if __name__ == "__main__":
	execApp = True
	execGui = True
	if len(sys.argv) > 1:
		for i, arg in enumerate(sys.argv):
			if arg == '-c' or arg == '--cli':
				execGui = False
			if arg == '-h' or arg == '--help':
				execApp = False

	if execApp:
		runApp(execGui)
	else:
		print("Hello stepwise processies application")
		print("")
		print("-c, --cli    Run in CLI mode.")
		print("-h, --help   Print help menu.")


