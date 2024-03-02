'''
Default Process Steps (v1.0.0)
Author(s): Chris Johnson (chrisjohn404)
September 2020
License: GPLv2
 - File defines a series of classes (steps), extending the "test" class
   ref "[app-root]/tp_core/test.py" and then links them together by
   extending the "testRunner" class which is also where application properties
   are configured.
'''

import threading
import time
from string import Template

from tp_core.test import Test
from tp_core.test_runner import TestRunner

DEBUG_ENABLED = False

'''
This is a step that will always pass illustrating returning messages to the user.
'''
class StepA(Test):
	def test(self, testRunner):
		if DEBUG_ENABLED:
			print('Starting Test', self.name, self.haltIfErr)

		try:
			li = ["Hello", "python", "World"]

			testRunner.global_variable = 0

			self.message = f'Step A Message: {li[0]} {li[2]}.'
			self.isComplete = True
		except:
			self.message = 'Step A Failure Message.'
			self.isErr = True
			self.isComplete = True

	def __init__(self, name, haltIfErr = False):
		self.haltIfErr = True
		Test.__init__(self, name, haltIfErr)

'''
This is a second step that will always pass.  The conditional test flag can be
be changed and the program will continue to run.  Note: this flag defaults to
true, a definable variable in the 'testManager' class at the bottom of the file.
'''
class StepB(Test):
	def test(self, testRunner):
		if DEBUG_ENABLED:
			print('Starting Test', self.name, self.haltIfErr)

		if False:
			self.message = "Step B failure message."
			self.isErr = True
		else:
			self.message = "Step B Message."

		self.isComplete = True

	def __init__(self, name, haltIfErr = False):
		self.haltIfError = False
		Test.__init__(self, name, haltIfErr)

'''
This test demonstrates how to perform a long-running task
and provide incremental user feedback.
'''
class StepC(Test):
	def test(self, testRunner):
		for i in range(10):
			time.sleep(0.1)
			self.update(i/10*100, "Working... "+str(i/10))

		self.message = "Step C Message."
		self.isComplete = True

	def __init__(self, name, haltIfErr = False):
		Test.__init__(self, name, haltIfErr)

'''
This test demonstrates how to prompt a tester to do something
during a test and providing an "Ok" button that has to be 
pressed before the application can continue.
'''
class StepD(Test):
	def test(self, testRunner):
		self.update(1, 'Waiting for test-runner to do something.')
		testRunner.displayMessage('My Title', 'My Incremental Message.', self.stepTwo)

	def stepTwo(self, testRunner, result):
		time.sleep(0.5)
		self.message = "Step D Message."
		self.isComplete = True

	def __init__(self, name, haltIfErr = False):
		Test.__init__(self, name, haltIfErr)

'''
This test demonstrates how to prompt a tester to do something
during a test and providing "OK" and "Cancel" buttons that has to be 
pressed before the application can continue.
'''
class StepE(Test):
	def msg_interpreter(self, user_input, gui_type):
		time.sleep(0.5)
		print('User Input:',user_input, gui_type)
		return user_input
	
	def test(self, testRunner):
		self.update(1, 'Waiting for test-runner to do something.')
		testRunner.displayMessage('User Prompt', 'Please do...', self.stepTwo, interpreter=self.msg_interpreter, messagebox_method='askokcancel')

	def stepTwo(self, testRunner, result):
		time.sleep(0.5)
		if result=='OK' or result=='' or result=='ok' or result==True:
			self.message = "Step E Message."
			self.isComplete = True
		else:
			self.message = "Step E Canceled." + str(result) + ':' + str(type(result))
			self.isComplete = True
			self.isErr = True

	def __init__(self, name, haltIfErr = False):
		Test.__init__(self, name, haltIfErr)

'''
This test demonstrates how to retry a test that has otherwise failed
and allowing the test to continue during a failed state.

Note: If retried 2x the test will pass.
'''
class StepF(Test):
	def msg_interpreter(self, user_input, gui_type):
		time.sleep(0.5)
		print('User Input:',user_input, gui_type)
		return user_input
	
	def test(self, testRunner):
		time.sleep(0.5)
		self.num_retries += 1
		if self.num_retries < 3:
			self.isErr = True
			self.update(round(self.num_retries/3*100,2), 'The test has failed... try number:' + str(self.num_retries))
			testRunner.displayMessage('Attempter...', 'Attempt: ' + str(self.num_retries) + ' has failed. Try again?', self.test, interpreter=self.msg_interpreter, messagebox_method='askretrycancel')
		else:
			self.isErr = False
			self.update(90, 'The test is still passing...')
			time.sleep(0.25)
			self.message = "Step F passed after " + str(self.num_retries) + " attempts."
			self.isComplete = True
	
	def __init__(self, name, haltIfErr = False):
		Test.__init__(self, name, haltIfErr)
		self.num_retries = 0

# Test Manager implements overall test set-up & teardown
# routines and contains a list of all of the tests.  It 
# extends the test-runner class
class TestManager(TestRunner):

	def getTestInfo(self):
		return {
			'name': 'Example Python Test Program',
			'version': '1.0.0',
			'author': 'chrisjohn404'
		}
	
	def getTestingInstructions(self):
		return '''1. Do something before running the program.
		2. Run program.
		'''

	def getTestInfoFmatTxt(self):
		tpString = '------------------------------------------------------------\n'
		tpString += '${name}: v${version}'
		return tpString
	
	def testingSetUp(self):
		'''
		No specific set-up is required
		@self: Required self function.
		'''
		return
	
	def testingTeardown(self):
		'''
		No specific tear-down is required.
		@self: Required self function.
		'''
		return

	# NOTE Function [tp_core/test_runner.py:'runTests'] gets called to run tests.
	def __init__(self):
		# Define tests.
		tests = [
			StepA('Step A Title', haltIfErr=True),
			StepB('Step B Title'),
			StepC('Step C Title'),
			StepD('Step D Title'),
			StepE('Step E Title'),
			StepF('Step F Title')
		]

		TestRunner.global_variable = 0

		TestRunner.__init__(self, tests, updateListener=self.defUpdateListener, finishedListener=self.defFinishedListener)





''' Author(s): Chris Johnson (chrisjohn404) '''