'''
Processie Executor (Implements "TestRunner")
Author(s): Chris Johnson
Circa 2020
 - Any implementor should extend this class in their process list to customize
   the resulting application.

 - Implements the "TestRunner" Class that executes defined processies, manages 
   each step's completion state/notification requests, and processes their
   output.  It notifies the executor via registered callbacks.
'''

from string import Template
import time


# Expand a string to fill a row.
def expandString(name, length):
    txt = name
    strLen = len(name)
    numToAdd = length - strLen

    for i in range(numToAdd):
        txt += ' '

    return txt
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class tstr:
    # inc = (f'{bcolors.OKBLUE}INCOMPLETE{bcolors.ENDC}')
    # fail = (f'{bcolors.FAIL}FAILED{bcolors.ENDC}')
    # passed = (f'{bcolors.OKGREEN}PASSED{bcolors.ENDC}')
    inc = (f'INCOMPLETE')
    fail = (f'FAILED')
    passed = (f'PASSED')

class TestRunner():
    # ------------ TestRunner Default Methods to be overridden START ----------------
    def getTestInfo(self):
        '''
        Default Class Function to be overridden defining default name object.
        @self: Required self argument.
        '''
        return {
            'name': 'Default Test Program',
            'version': '-1.-1.-1'
        }

    def getTestInfoFmatTxt(self):
        '''
        Default Class Function to be overridden defining default in-messagebox- header.
        @self: Required self argument.
        '''
        return '''------------------------------------------------------------
        Test Program Version: ${version}'''
    
    def testingSetUp(self):
        '''
        Function that gets executed before any tests are run
        @self: Required self argument.
        '''
        print("Default Testing Set-up")

    def testingTeardown(self):
        '''
        Function that gets executed after all tests have finished running
        @self: Required self argument.
        '''
        print("Default Testing Tear-down")
    # ------------ TestRunner Default Methods to be overridden END ------------------
    # --------------------------------------------------------------------------

    def getCurStateText(self):
        '''
        Externally callable function that queries for test runner's current
        state.
        @self: Required self argument.
        '''
        txt = ''
        

        testInfo = self.getTestInfo()
        testFmatStr = Template(self.getTestInfoFmatTxt())
        overallPassed = True
        overallComplete = True
        incompleteFailed = False
        txt += testFmatStr.substitute(testInfo)
        txt += '\n\n'

        columns = ['name', 'status', 'message']
        columnWidths = [30, 10, 80]

        txt += expandString(columns[0], columnWidths[0])
        txt += '| '
        txt += expandString(columns[1], columnWidths[1])
        txt += '| '
        txt += expandString(columns[2], columnWidths[2])
        txt += '\n'

        for test in self.tests:
            txt += expandString(test.name,columnWidths[0])
            txt += '| '

            if not test.isComplete:
                overallComplete = False
                overallPassed = False
                if test.percentComplete > 0:
                    t = Template('${percentComplete}%')

                    txt += expandString(
                        t.substitute(
                            {'percentComplete':test.percentComplete}
                        ), columnWidths[1])
                else:
                    txt += expandString(tstr.inc, columnWidths[1])
            else:
                if test.isErr:
                    overallPassed = False
                    txt += expandString(tstr.fail, columnWidths[1])

                    if test.haltIfErr:
                        incompleteFailed = True
                else:
                    txt += expandString(tstr.passed, columnWidths[1])
            txt += '| '
            txt += test.message
            txt += '\n'

        txt += '\nOverall Result: '
        if overallComplete:
            if overallPassed:
                txt += 'PASSED. Duration: ' + str(self.getCompletedTimeDiffInSec()) + 's'
            else:
                txt += 'FAILED. Duration: ' + str(self.getCompletedTimeDiffInSec()) + 's'
        else:
            if self.isRunning:
                if incompleteFailed:
                    txt += 'FAILED. Duration: ' + str(self.getCompletedTimeDiffInSec()) + 's'
                else:
                    txt += 'INCOMPLETE. Duration: ' + str(self.getCurTimeDiffInSec()) + 's'
            else:
                txt += 'Not Started.'
        return txt

    # --------------------------------------------------------------------------
    # ------------ Class Functions to set-up and run tests START ---------------
    def initTests(self):
        '''
        @self: Required self argument.
        '''
        # Clear previous test resunts
        for test in self.tests:
            test.clear()

        self.startTime = 0
        self.finishedTime = 0
        self.isRunning = False
    
    def runTests(self):
        '''
        Function that kicks off all of the tests.
        @self: Required self argument.
        '''
        self.initTests()
        self.isRunning = True
        self.startTime = time.time()
        self.finishedTime = 0

        # Start testing routine
        self.testingSetUp()

        # Execute each test
        for test in self.tests:
            try:
                test.runTest(self, self.tests, self.updateCB)
            except:
                # If an un-caught software error occured, catch it & stop testing.
                test.message = 'Uncaught software exception, test failed.'
                test.isErr = True
                test.haltIfErr = True

            # If needed, stop executing remaining tests
            if test.isErr:
                if test.haltIfErr:
                    break

            # Begine code to... Indicate that test has finished & trigger a GUI update event
            self.finishedFunc(self.tests)

        # Call the "finished func" a second time to indicate testing is complete.
        self.finishedTime = time.time()
        self.finishedFunc(self.tests)

        self.testingTeardown()

        passed = True
        for test in self.tests:
            if test.isErr:
                passed = False

        if passed:
            self.numSuccessfulIterations += 1
        self.numIterations += 1

        self.isRunning = False
        return passed

    def getCompletedTimeDiffInSec(self):
        '''
        @self: Required self argument.
        '''
        # TODO: The self.finishedTime doesn't get populated correctly for report...
        delta = self.finishedTime - self.startTime
        return round(delta,3)
    def getCurTimeDiffInSec(self):
        '''
        @self: Required self argument.
        '''
        curTime = time.time()
        delta = curTime - self.startTime
        return round(delta,3)
    # ------------ Class Functions to set-up and run tests START ---------------
    # --------------------------------------------------------------------------


    # --------------------------------------------------------------------------
    # ------------------- Class Property Getters, START ------------------------
    def getTests(self):
        '''
        @self: Required self argument.
        '''
        return self.tests
    def getNumTests(self):
        '''
        @self: Required self argument.
        '''
        return len(self.tests)
    def getNumCompleteTests(self):
        '''
        @self: Required self argument.
        '''
        numComplete = 0
        for test in self.tests:
            if test.isComplete:
                numComplete += 1
        return numComplete
    # ------------------- Class Property Getters, END --------------------------
    # --------------------------------------------------------------------------
    
    def updateCB(self, test):
        '''
        @self: Required self argument.
        @test: Referenced test class.
        '''
        self.updateFunc(self.tests, test)

    def testReporter(self, testDef, isErr=False, message =''):
        '''
        Test Reporter UCF
        @self: Required self argument.
        @testDef: Object being populated.
        '''
        testDef.isErr = isErr
        testDef.message = message

    # --------------------------------------------------------------------------
    # ------------------- Class Spec Callback Defaults, START ------------------
    def defUpdateListener(self, testStatusInfo, curTest):
        '''
        Class spec default callback function overridden during instansiation to
        pass incremental step/"test" updates.

        @self: Required self argument.
        '''
        print("DEFAULT FUNC: Received Test Update")

    def defFinishedListener(self, testStatusInfo):
        '''
        Class spec default callback function overridden during instansiation to
        pass step/"test" complete updates.

        @self: Required self argument.
        '''
        print("DEFAULT FUNC: Test Finished")

    def defDisplayMessage(self, title, message, cb):
        '''
        Class spec default callback function overridden during instansiation to
        update message..

        @self: Required self argument.
        '''
        print("DEFAULT FUNC: Displaying Message", title, message)
        cb(self)
    
    # ------------------- Class Spec Callback Defaults, END --------------------
    
    def attachListeners(self, updateListener=None, finishedListener=None, displayMessage=None):
        '''
        Function to be externally called to update listeners prior to init.
        @self: Required self argument.
        '''
        if updateListener is None:
            self.updateFunc = self.defUpdateListener
        else:
            self.updateFunc = updateListener

        if finishedListener is None:
            self.finishedFunc = self.defFinishedListener
        else:
            self.finishedFunc = finishedListener

        if displayMessage is None:
            self.displayMessage = self.defDisplayMessage
        else:
            self.displayMessage = displayMessage
    # ------------------- Class Spec Callback Defaults, START ------------------
    # --------------------------------------------------------------------------

    def __init__(self, tests, updateListener=None, finishedListener=None, displayMessage=None):
        '''
        Function that gets called after each test to update the test status
        object and notify listeners...

        @self: Required self argument.
        '''
        self.tests = tests

        if updateListener is None:
            self.updateFunc = self.defUpdateListener
        else:
            self.updateFunc = updateListener

        if finishedListener is None:
            self.finishedFunc = self.defFinishedListener
        else:
            self.finishedFunc = finishedListener

        if displayMessage is None:
            self.displayMessage = self.defDisplayMessage
        else:
            self.displayMessage = displayMessage

        self.numIterations = 0
        self.numSuccessfulIterations = 0
        self.isRunning = False
        self.startTime = 0
        self.finishedTime = 0

        self.initTests()

    def destroy(self):
        print("Shutting Down Test Runner")

# tester = testRunner()
# tester.run()


''' Author(s): Chris Johnson (chrisjohn404) Circa 2020'''

