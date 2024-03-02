'''
CLI GUI Test Runner (Implements "CliTestApplication")
Author: Chris Johnson (chrisjohn404)
September 2020
License: GPLv2
 - Implements the "CliTestApplication" class which runs a set of defined tests
   and produces a CLI gui.
'''

import sys

class CliTestApplication():
	# Arg testRunner: an initialized test runner class
	def __init__(self, testRunner):
		'''
		Initialize test runner and pass callback functions.

		@self: Required self argument.
		@testRunner: Initialized [tests.py].testManager reference
		'''

		self.testRunner = testRunner
		self.testRunner.attachListeners(
		  updateListener=self.updateListener,
		  finishedListener=self.finishedListener,
		  displayMessage=self.displayMessage
		)

	# --------------------------------------------------------------------------
	# ---------- Defining Callbacks and associated methods START ---------------
	def updateListener(self, testStatusInfo, curTest):
		'''
		A callback method which updates the GUI when an incremental update needs
		to occur.  Updates the GUI's text box and other indicators.
		
		@self: Required self argument.
		@testStatusInfo: Object representing current state of test.
		@curTest: Object representing current test being executed.
		'''

		if True:
			self.clearCliWindow()
			print(self.testRunner.getCurStateText())

	def finishedListener(self, testStatusInfo):
		'''
		A callback method which updates the GUI when a processie finishes
		executing.  Updates the GUI's text box and other indicators.

		@self: Required self argument.
		@testStatusInfo: Object representing current state of test.
		'''

		if True:
			self.clearCliWindow()
			print(self.testRunner.getCurStateText())

	def displayMessage(self, title, message, cb, interpreter=None, messagebox_method=''):
		'''
		A callback method that displays a pop-up message to the executor with an
		"OK" button; delays the process step until pressed.
		
		@self: Required self argument.
		@title: Title of message window.
		@message: Message to be displayed.
		@cb: Method called to resume step execution.
		'''

		print('')
		print('')
		print('- [' + title + ']: ' + message)
		print('[Press enter to continue]')
		print('[Press ctrl+c to exit]')
		result = 'OK'
		if interpreter:
			result = input('-->')
			result = interpreter(result, 'cli')
		else:
			result = input('-->')
		
		try:
			cb(self.testRunner, result)
		except:
			cb(self.testRunner)

	# ------------------- Callbacks END, Called Methods START ------------------
	def startTest(self):
		'''
		Function that starts running defined steps (test class extensions).

		@self: Required self argument.
		'''
		print("Starting Test (cli app)")
		self.testRunner.runTests()
		print("Testing Finished")

	def clearCliWindow(self):
		'''
		Function that clears screen.

		@self: Required self argument.
		'''
		for i in range(43):
			print("")
	# ---------- Defining Callbacks and associated methods END -----------------
	# --------------------------------------------------------------------------
	


		
	



''' Author(s): Chris Johnson (chrisjohn404) September 2020'''