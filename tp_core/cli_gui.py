'''
CLI GUI Test Runner
- Runs a set of defined tests and produces a CLI gui.
Author(s): Chris Johnson
September 2019


'''

import sys

class CliTestApplication():

    def startTest(self):
        print("Starting Test (cli app)")
        self.testRunner.runTests()
        print("Testing Finished")

    def clearCliWindow(self):
        for i in range(30):
            print("")

    def updateListener(self, testStatusInfo, curTest):
        if True:
            self.clearCliWindow()
            print(self.testRunner.getCurStateText())

    def finishedListener(self, testStatusInfo):
        if True:
            self.clearCliWindow()
            print(self.testRunner.getCurStateText())

    def displayMessage(self, title, message, cb):
        print('')
        print('')
        print('- [' + title + ']: ' + message)
        print('[Press enter to continue]')
        text = input('-->')
        cb(self.testRunner)
        
    # Arg testRunner: an initialized test runner class
    def __init__(self, testRunner):
        self.testRunner = testRunner
        self.testRunner.attachListeners(
          updateListener=self.updateListener,
          finishedListener=self.finishedListener,
          displayMessage=self.displayMessage
        )





