
from string import Template
import time

'''
The general procedure for testing the ESP32 is:
1. Establish sign-of-life by reading
2. 
'''
def expandString(name, length):
    txt = name
    strLen = len(name)
    numToAdd = length - strLen

    for i in range(numToAdd):
        txt += ' '

    return txt

class testRunner():
    # Function that gets called after each test to update the
    # test status object and notify listeners...
    def testReporter(self, testDef, isErr=False, message =''):
        testDef.isErr = isErr
        testDef.message = message

    # Default Update Listener function, should be attached to by
    # a GUI interface to notify users that an incremental test
    # update has been received.
    def defUpdateListener(self, testStatusInfo, curTest):
        print("DEFAULT FUNC: Received Test Update")

    # Default "Test Finished" function, should be attached to by
    # a GUI interface to notify users that a complete test step 
    # has been accomplished.
    def defFinishedListener(self, testStatusInfo):
        print("DEFAULT FUNC: Test Finished")

    # Default "Display Message" function.
    def defDisplayMessage(self, title, message, cb):
        print("DEFAULT FUNC: Displaying Message", title, message)
        cb(self)

    def getTestInfo(self):
        return {
            'name': 'Default Test Program',
            'version': '-1.-1.-1'
        }
    def getTestInfoFmatTxt(self):
        return '''------------------------------------------------------------
        Test Program Version: ${version}'''

    def getCurStateText(self):
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
                    txt += expandString('INCOMPLETE', columnWidths[1])
            else:
                if test.isErr:
                    overallPassed = False
                    txt += expandString('FAILED', columnWidths[1])

                    if test.haltIfErr:
                        incompleteFailed = True
                else:
                    txt += expandString('PASSED', columnWidths[1])
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

    def updateCB(self, test):
        self.updateFunc(self.tests, test)

    def getCurTimeDiffInSec(self):
        curTime = time.time()
        delta = curTime - self.startTime
        return round(delta,3)

    def getCompletedTimeDiffInSec(self):
        # TODO: The self.finishedTime doesn't get populated correctly for report...
        delta = self.finishedTime - self.startTime
        return round(delta,3)

    def initTests(self):
        # Clear previous test resunts
        for test in self.tests:
            test.clear()

        self.startTime = 0
        self.finishedTime = 0
        self.isRunning = False
        
    # Function that kicks off all of the tests.
    def runTests(self):
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

    # Function that gets executed before any tests are run
    def testingSetUp(self):
        print("Default Testing Set-up")

    # Function that gets executed after all tests have finished
    # running
    def testingTeardown(self):
        print("Default Testing Tear-down")

    def getTests(self):
        return self.tests
    def getNumTests(self):
        return len(self.tests)
    def getNumCompleteTests(self):
        numComplete = 0
        for test in self.tests:
            if test.isComplete:
                numComplete += 1
        return numComplete

    def attachListeners(self, updateListener=None, finishedListener=None, displayMessage=None):
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


    def __init__(self, tests, updateListener=None, finishedListener=None, displayMessage=None):
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