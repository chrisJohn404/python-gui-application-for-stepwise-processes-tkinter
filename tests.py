'''
ESP32 Test Program
Author(s): Chris Johnson
September 2019


'''

import threading
import time
from string import Template

from tp_core.test import test
from tp_core.test_runner import testRunner

DEBUG_ENABLED = False


'''
This is a step that will always pass illustrating returning messages to the user.
'''
class stepA(test):
    def test(self, testRunner):
        if DEBUG_ENABLED:
            print('Starting Test', self.name, self.haltIfErr)

        try:
            hi = ["Hello", "python", "World"]

            testRunner.global_variable = 0

            msgTemplate = Template('''Step A Message: ${first_arg} ${second_arg}.''')

            self.message = msgTemplate.substitute({
                'first_arg': hi[0],
                'second_arg': hi[2]
            })
            self.isComplete = True
        except:
            self.message = 'Step A Failure Message.'
            self.isErr = True
            self.isComplete = True

    def __init__(self, name, haltIfErr = False):
        self.haltIfErr = True
        test.__init__(self, name, haltIfErr)


'''
This is a second step that will always pass.  The conditional test flag can be
be changed and the program will continue to run.  Note: this flag defaults to
true, a definable variable in the 'testManager' class at the bottom of the file.
'''
class stepB(test):
    def test(self, testRunner):
        if DEBUG_ENABLED:
            print('Starting Test', self.name, self.haltIfErr)

        if False:
            self.message = "Step B failure message."
            self.isErr = True
        else:
            self.message = "Step B succeeded."

        self.isComplete = True

    def __init__(self, name, haltIfErr = False):
        self.haltIfError = False
        test.__init__(self, name, haltIfErr)

'''
This test demonstrates how to perform a long-running task
and provide incremental user feedback.
'''
class stepC(test):
    def test(self, testRunner):
        for i in range(10):
            time.sleep(0.1)
            self.update(i/10*100, "Working... "+str(i/10))

        self.message = "Step C is complete."
        self.isComplete = True

    def __init__(self, name, haltIfErr = False):
        test.__init__(self, name, haltIfErr)

'''
This test demonstrates how to prompt a tester to do something
during a test and providing an "Ok" button that has to be 
pressed before the application can continue.
'''
class stepD(test):
    def test(self, testRunner):
        self.update(1, 'Notifying test-runner to do something.')
        testRunner.displayMessage('Title... (My Title)', 'Message... (My Message).', self.stepTwo)

    def stepTwo(self, testRunner):
        time.sleep(0.5)
        self.message = "Step D Message"
        self.isComplete = True

    def __init__(self, name, haltIfErr = False):
        test.__init__(self, name, haltIfErr)

'''
This test demonstrates how to prompt a tester to do something
during a test and providing an "Ok" button that has to be 
pressed before the application can continue.
'''
class stepE(test):
    def test(self, testRunner):
        self.message = f"Step E Message: {testRunner.global_variable}"
        self.isComplete = True

    def __init__(self, name, haltIfErr = False):
        test.__init__(self, name, haltIfErr)


# Test Manager implements overall test set-up & teardown
# routines and contains a list of all of the tests.  It 
# extends the test-runner class
class testManager(testRunner):
    def testingSetUp(self):
        # No specific set-up is required.
        return

    def getTestInfo(self):
        return {
            'name': 'Example Python Test Program',
            'version': '1.0.0'
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

        tests = [
            stepA('Step A Title', haltIfErr=True),
            stepB('Step B Title'),
            stepC('Step C Title'),
            stepD('Step D Title'),
            stepE('Step E Title')
        ]

        testRunner.global_variable = 0

        testRunner.__init__(self, tests, updateListener=self.defUpdateListener, finishedListener=self.defFinishedListener)

