'''
Process Steps (Example #1, v1.0.0)
Author(s): Chris Johnson (chrisjohn404)
September 2020
License: GPLv2
 - File defines a series of classes (steps), extending the "test" class
   ref "[app-root]/tp_core/test.py" and then links them together by
   extending the "testRunner" class which is also where application properties
   are configured.
'''

import sys
import os
from os import path
import importlib.util

import threading
import time
from string import Template

from test import Test
from test_runner import TestRunner

DEBUG_ENABLED = False

'''
This is a step that will always pass illustrating returning messages to the user.
'''
class stepA(Test):
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
class stepB(Test):
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
class stepC(Test):
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
class stepD(Test):
    def test(self, testRunner):
        self.message = f"Step E Message: {testRunner.global_variable}."
        self.isComplete = True

    def __init__(self, name, haltIfErr = False):
        Test.__init__(self, name, haltIfErr)


# Test Manager implements overall test set-up & teardown
# routines and contains a list of all of the tests.  It 
# extends the test-runner class
class testManager(TestRunner):
    def testingSetUp(self):
        # No specific set-up is required.
        return

    def getTestInfo(self):
        return {
            'name': f'Example User Defined Python Test Program: \"{path.basename(__file__)}\"',
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

    # There is a function: runTests that runs the tests
    def testingTeardown(self):
        # No specific tear-down is required.
        return

    def __init__(self):
        # Define tests.
        tests = [
            stepA('Step A Title', haltIfErr=True),
            stepB('Step B Title'),
            stepC('Step C Title'),
            stepD('Step D Title'),
            stepC('Step C.2 Title'),
        ]

        # Need to define a process scoped global?
        TestRunner.global_variable = 0

        # Init TestRunner.
        TestRunner.__init__(self, tests, updateListener=self.defUpdateListener, finishedListener=self.defFinishedListener)


''' Author(s): Chris Johnson (chrisjohn404) September 2020'''