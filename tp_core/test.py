'''
Step  (Implements "Test")
Author(s): Chris Johnson (chrisjohn404)
September 2020
License: GPLv2
 - Implements the "Test" class which any implementor should extend as a ~step~
   of their defined process.
'''


class Test():
    # This is a default test function that serves as a
    # very basic example for what a test should look like.
    # THIS FUNCTION SHOULD BE RE-DEFINED BY USER
    def test(self):
        print("Default Test, should be overwritten/extended. Reporting error.")
        self.update(50, "Default Test Status Update")
        self.finished(isErr = True, message="Default test finished, test was not defined.")


    # THE REMAINING FUNCTIONS SHOULD NOT BE RE-DEFINED...
    # Function that gets called 
    def finished(self, isErr = False, message=''):
        self.isErr = isErr
        self.isComplete = True
        self.message = message
        self.percentComplete = 100

        self.stopTime = 0 # TODO: GET CURRENT TIME
        self.duration = self.stopTime - self.startTime

        # Report that test has been finished.  Trigger an event...
    
    def update(self, percentComplete, message):
        self.percentComplete = percentComplete
        self.message = message

        # Report that the test has an updated message/status.
        self.updateFunc(self)
    
    # This function gets called by the test runner & calls the
    # defined test.
    def runTest(self, testRunner, tests, updateFunc):
        self.startTime = 0 # TODO: GET CURRENT TIME
        self.updateFunc = updateFunc
        self.test(testRunner)

    def clear(self):
        self.isErr = False
        self.message = ''
        self.isComplete = False
        self.percentComplete = 0
        self.startTime = 0
        self.stopTime = 0
        self.duration = 0

    def __init__(self, name, haltIfErr = False):
        self.name = name
        self.haltIfErr = haltIfErr
        self.isErr = False
        self.message = ''
        self.isComplete = False
        self.percentComplete = 0

        self.startTime = 0
        self.stopTime = 0
        self.duration = 0




''' Author(s): Chris Johnson (chrisjohn404) September 2020'''