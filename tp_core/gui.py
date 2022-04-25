
'''
Test Application GUI

Author: Chris Johnson
Date: December 2019

This is a basic GUI manager that executes defined tests.
'''

from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import messagebox
import sys
import threading
import time


'''
Define a class that manages the execution of a process in a
unique thread.
'''
class testingThread(threading.Thread):
    def __init__(self, threadID, name, testRunner, completeCB=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.testRunner = testRunner

        if completeCB is None:
            self.completeCB = self.defaultCompleteCB
        else:
            self.completeCB = completeCB

    def defaultCompleteCB(self, passed):
        return

    def shutdown(self):
        self.stopService = True

    def run(self):
        passed = self.testRunner.runTests()
        if self.completeCB:
            self.completeCB(passed)

class TestApplication(Frame):
    '''
    Define initialization function.
    @self: Required self argument.
    @testRunner: Initialized [tests.py].testManager reference
    @master: tkinter root reference.
    '''
    def __init__(self, testRunner, master=None):
        self.testRunner = testRunner
        self.testRunner.attachListeners(
          updateListener=self.updateListener,
          finishedListener=self.finishedListener,
          displayMessage=self.showMessageBox
        )

        self.master = master
        self.master.title(self.testRunner.getTestInfo()['name'])
        
        self.frame = Frame.__init__(self, master,width=480, height=280,bg='#999999')
        
        # Define keyboard shortcuts.
        self.master.bind('<F2>', lambda event: self.startTest())
        self.master.bind('R', lambda event: self.startTest())
        self.master.bind('<F4>', lambda event: self.quit())
        self.master.bind('Q', lambda event: self.quit())

        self.pack()
        self.createHeader()
        self.createWidgets()

        self.testStatusMessage = 'Not Running'

    '''
    Define function that enables the test status message box to be updated.
    '''
    def updateStatusMessage(self, msg=None):
        if msg is None:
            msg = self.testStatusMessage

        self.testStatusMessage = msg
        self.overallTestStatus['state']='normal'
        self.overallTestStatus.delete("0","end")
        self.overallTestStatus.insert(0, msg)
        self.overallTestStatus['state']='readonly'

    '''
    Define a function that gets called to update:
     - The "Progress" bar
     - The "Overall Status" message box
    '''
    def updateProgress(self):
        numTests = self.testRunner.getNumTests()
        numCompleteTests = self.testRunner.getNumCompleteTests()
        percentComplete = (numCompleteTests/numTests)*100
        self.progressBar['value'] = percentComplete

        statusText = 'Running: '
        statusText += str(numCompleteTests) + '/' + str(numTests)
        self.updateStatusMessage(statusText)

    '''
    Define a function that gets called to update the GUI's text
    box (the status of the stepwise process), and then update 
    the other indicators.  An incremental update function...
    '''
    def updateListener(self, testStatusInfo, curTest):
        self.textBox.delete('1.0',tk.END)
        self.textBox.insert('1.0',self.testRunner.getCurStateText())
        self.updateProgress()
    '''
    Define a function that gets called to update the GUI's text
    box (the status of the stepwise process), and then update 
    the other indicators.  To be executed when a test step
    is finished.
    '''
    def finishedListener(self, testStatusInfo):
        self.textBox.delete('1.0',tk.END)
        self.textBox.insert('1.0',self.testRunner.getCurStateText())
        self.updateProgress()

    '''
    Define a function that lets a test display a message box to 
    the user.
    '''
    def showMessageBox(self, title, message, cb):
        messagebox.showinfo(title, message)
        cb(self.testRunner)

    '''
    Define a function that gets executed whe a test is completed
    which prints slightly different information than the 
    "updateListener" and "finishedListener" functions.  To be 
    executed when all steps complete.
    '''
    def testComplete(self, passed):
        self.updateProgress()
        numTestExecutions = self.testRunner.numIterations
        numSuccTestExecs = self.testRunner.numSuccessfulIterations
        msg = str(numSuccTestExecs) + '/' + str(numTestExecutions)
        msg += ' Completed Tests'
        self.updateStatusMessage(msg)

    '''
    Define a function that starts running the tests.
    '''
    def startTest(self):
        self.testRunner.initTests()
        self.updateProgress()

        self.testThread = testingThread(3, "GUI_TEST_THREAD", self.testRunner, self.testComplete)
        self.testThread.start()
    '''
    Define a function that quits tkinter.
    '''
    def quit(self):
        sys.exit()
    
    '''
    Define a function that sets up the top portion of the test application.
    ''' 
    def createHeader(self):
        self.header = Frame(self)
        self.header.pack({'fill':'both', 'expand':'true'})

        self.appLabel = Label(self.header)
        self.appLabel['text'] = self.testRunner.getTestInfo()['name']
        self.appLabel.pack({'padx':10, 'pady':10, 'fill':'x', 'expand':'false', 'side':'left'})

        self.versionLabel = Label(self.header)
        self.versionLabel['text'] = self.testRunner.getTestInfo()['version']
        self.versionLabel.pack({'padx':10, 'pady':10, 'fill':'x', 'expand':'false', 'side':'right'})

        self.lowHdr = Frame(self)
        self.lowHdr.pack({'fill':'both','expand':'true'})
        self.progressLabel = Label(self.lowHdr)
        self.progressLabel['text'] = 'Progress:'
        self.progressLabel.pack({'padx':10,'fill':'both','side':'left'})

        ## Add Colored progress bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        self.progressBar = Progressbar(self.lowHdr, length=300, style='black.Horizontal.TProgressbar')
        self.progressBar['value'] = 0
        self.progressBar.pack({'padx':10,'side':'left','expand':'false'})

        self.overallTestStatus = tk.Entry(self.lowHdr,
            width=20,
            state='normal',
            textvariable='Not Running',
            text='Not Running'
        )

        self.overallTestStatus.pack({'padx':5,'side':'right'})
        self.updateStatusMessage('Not Running')
        self.overallTestStatus['state']='readonly'

        self.statusTextLabel = Label(self.lowHdr)
        self.statusTextLabel['text'] = 'Overall Status:'
        self.statusTextLabel.pack({'padx':10,'side':'right'})

    '''
    Define a function that sets up the window's text-box and run/quit buttons.
    '''
    def createWidgets(self):
        self.textBox = tkst.ScrolledText(
            master = self,
            wrap= WORD,
            width=100,
            height=30
        )

        self.textBox.pack(padx=10, pady=10, fill=BOTH, expand=True)
        defaultString = self.testRunner.getCurStateText()
        self.textBox.insert(INSERT, defaultString)

        style = ttk.Style() 
        style.configure('TButton', foreground="red") 
        style.map("TButton",
          foreground=[('pressed', 'red'), ('active', 'red')],
          background=[('pressed', '!disabled', 'black'),
                      ('active', 'white')]
        )

        self.runButton = tk.Button(self,width=20, height=2)
        self.runButton["text"] = "Run <F2>",
        self.runButton["command"] = self.startTest
        self.runButton.pack({"side": "left",'padx':10,'pady':10})

        self.QUIT = tk.Button(self, width=20, height=2)
        self.QUIT["text"] = "QUIT <F4>"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "right",'padx':10})

'''
Define a function to be called externally that executes the application.
'''
def TestApplicationInit(testRunner):
    root = Tk()
    app = TestApplication(testRunner, master=root)
    app.mainloop()
    root.destroy()
    return {'root':root,'app':app}







