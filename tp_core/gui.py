'''
Test Application GUI (Implements "TestApplication")
Author: Chris Johnson (chrisjohn404)
September 2020
License: GPLv2
 - Implements the "TestApplication" class which extends tkinter's "Frame" class
   to implement the gui.
'''


from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import messagebox
import sys
import threading
import time, re

from colors import tclInterpretationCodes
from colors import stripAnsiEscapeSequences



class TestApplication(Frame):
	def __init__(self, testRunner, master=None):
		'''
		Initialize test runner and pass callback functions.  Setup Tkinter GUI,
		attach short-cut keys, and create GUI elements.

		@self: Required self argument.
		@testRunner: Initialized [tests.py].testManager reference
		@master: tkinter root reference.
		'''

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

	# Callbacks & Methods, Interior Functions, Tk Widget Initialization.
	# --------------------------------------------------------------------------
	def updateAndFormatTextBox(self, ansi_text):
		'''
		A method which updates the textBox GUI element
		'''
		self.textBox.delete('1.0',tk.END)
		self.textBox.insert('1.0',stripAnsiEscapeSequences(ansi_text))
		completed_tags = []
		tags = []
		chars_buf = ''
		null_char = '\033'
		char_chk = [
			null_char,
			'\033['
		]
		line_num = 1
		line_offset = 1
		r = re.compile("\033\[[;\d]*[A-Za-z]")
		for i in range(0, len(ansi_text)):
			increment_counter = True
			
			if len(chars_buf) < 1:
				if ansi_text[i] == null_char:
					increment_counter = False
					chars_buf = null_char
					# continue
			elif len(chars_buf) < len(char_chk):
				chars_buf = chars_buf + ansi_text[i]
				if chars_buf != char_chk[len(chars_buf)-1]:
					chars_buf = ''
			elif not r.search(chars_buf):
				increment_counter = False
				# print('Working on a tag...', len(chars_buf))
				chars_buf = chars_buf + ansi_text[i]
			elif r.search(chars_buf):
				increment_counter = False
				# print('Found a completed tag and have the next character.')
				if chars_buf == '\033[0m':
					# print('We have an end-tag... and have the next character.')
					last_tag = tags.pop()
					last_tag["end_tag_end_offset"] = i
					last_tag["end_tag_start_offset"] = i - len(chars_buf),
					last_tag["tag_diff"] = line_offset - last_tag["tag_line_offset"]
					completed_tags.append(last_tag)
				else:
					# print('We have a new tag and have the next character.', len(chars_buf), chars_buf[1:])
					tags.append({
						"tag_str": chars_buf,
						"tag_line": line_num,
						"tag_line_offset": line_offset,
						"start_tag_end_offset": i,
						"start_tag_start_offset": i - len(chars_buf),
						"end_tag_end_offset": i,
						"end_tag_start_offset": i - len(chars_buf),
						"tag_diff": 0,
					})
				chars_buf = ''
				chars_buf = chars_buf + ansi_text[i]
			
			# print('proc..',ansi_text[i], ansi_text[i] == null_char, len(chars_buf), increment_counter)
			if increment_counter:
				line_offset += 1
				if ansi_text[i] == '\n':
					line_num += 1
					line_offset = 1
				if ansi_text[i] == '\r':
					line_offset = 1

		# print('HERERE', len(ansi_text))
		tag_id = 0
		for tag in completed_tags:
			tag_id += 1
			tag_str = "start_"+str(tag_id)

			# print(tag_str, f'{tag["tag_line"]}.{tag["tag_line_offset"]}', f'{tag["tag_line"]}.{tag["tag_line_offset"]+tag["tag_diff"]}')
			self.textBox.tag_add(tag_str, f'{tag["tag_line"]}.{tag["tag_line_offset"]-2}', f'{tag["tag_line"]}.{tag["tag_line_offset"]+tag["tag_diff"]-2}')
			bg = "white"
			fg = "black"
			pure_nums_str = tag["tag_str"][2:len(tag["tag_str"])-1]
			for nums_str in pure_nums_str.split(';'):
				if tclInterpretationCodes[nums_str]["fg"]:
					fg = tclInterpretationCodes[nums_str]["color"]
				if tclInterpretationCodes[nums_str]["bg"]:
					bg = tclInterpretationCodes[nums_str]["color"]
			self.textBox.tag_config(tag_str, background=bg,foreground=fg)	

		# self.textBox.tag_add("start","1.8","1.13")
		# self.textBox.tag_config("start", background="white",foreground="black")
		# https://www.oreilly.com/library/view/python-in-a/0596001886/re672.html



	# ---------- Defining Callbacks and associated methods START ---------------
	def updateListener(self, testStatusInfo, curTest):
		'''
		A callback method which updates the GUI when an incremental update needs
		to occur.  Updates the GUI's text box and other indicators.
		
		@self: Required self argument.
		@testStatusInfo: Object representing current state of test.
		@curTest: Object representing current test being executed.
		'''
		self.updateAndFormatTextBox(self.testRunner.getCurStateText())
		self.updateProgress()
		
	def finishedListener(self, testStatusInfo):
		'''
		A callback method which updates the GUI when a processie finishes
		executing.  Updates the GUI's text box and other indicators.

		@self: Required self argument.
		@testStatusInfo: Object representing current state of test.
		'''
		# self.textBox.delete('1.0',tk.END)
		# self.textBox.insert('1.0',self.testRunner.getStrippedCurStateText())
		# self.textBox.tag_add("start","1.8","1.13")
		# self.textBox.tag_config("start", background="black",foreground="red")
		self.updateAndFormatTextBox(self.testRunner.getCurStateText())
		self.updateProgress()

	def showMessageBox(self, title, message, cb, interpreter=None, messagebox_method='showinfo'):
		'''
		A callback method that displays a pop-up message to the executor with an
		"OK" button; delays the process step until pressed.

		Documentation for messagebox methods:
		https://docs.python.org/3/library/tkinter.messagebox.html#messagebox-types
		ex: `messagebox.showinfo(title, message)`
		
		@self: Required self argument.
		@title: Title of message window.
		@message: Message to be displayed.
		@cb: Method called to resume step execution.
		'''
		method = getattr(messagebox, messagebox_method)

		if interpreter:
			result = interpreter(method(title, message), 'tkinter')
		else:
			result = method(title, message)
		
		try:
			cb(self.testRunner, result)
		except:
			cb(self.testRunner)
	# ------------------- Callbacks END, Called Methods START ------------------
	def updateProgress(self):
		'''
		Function which updates the "Progress" bar and executes method to update
		"Overall Status" text box.

		@self: Required self argument.
		'''
		numTests = self.testRunner.getNumTests()
		numCompleteTests = self.testRunner.getNumCompleteTests()
		percentComplete = (numCompleteTests/numTests)*100
		self.progressBar['value'] = percentComplete

		statusText = 'Running: '
		statusText += str(numCompleteTests) + '/' + str(numTests)
		self.updateStatusMessage(statusText)

	def updateStatusMessage(self, msg=None):
		'''
		Function that updates the text displayed in the "Overall Status" text
		box.

		@self: Required self argument.
		@msg: A string to be displayed in the status message box.
		'''
		if msg is None:
			msg = self.testStatusMessage

		self.testStatusMessage = msg
		self.overallTestStatus['state']='normal'
		self.overallTestStatus.delete("0","end")
		self.overallTestStatus.insert(0, msg)
		self.overallTestStatus['state']='readonly'
	# ---------- Defining Callbacks and associated methods END -----------------
	# --------------------------------------------------------------------------

	def startTest(self):
		'''
		Function that starts running defined steps (test class extensions).

		@self: Required self argument.
		'''
		self.testRunner.initTests()
		self.updateProgress()

		self.testThread = testingThread(3, "GUI_TEST_THREAD", self.testRunner, self.testComplete)
		self.testThread.start()
	
	def testComplete(self, passed):
		'''
		A callback method executed upon process iteration completion.  Displays
		tailored information to completion.

		@self: Required self argument.
		@passed: Boolean indicating process overall result.
		'''
		self.updateProgress()
		numTestExecutions = self.testRunner.numIterations
		numSuccTestExecs = self.testRunner.numSuccessfulIterations
		msg = str(numSuccTestExecs) + '/' + str(numTestExecutions)
		msg += ' Completed Tests'
		self.updateStatusMessage(msg)

	def quit(self):
		'''
		Define a function that quits tkinter.

		@self: Required self argument.
		'''
		sys.exit()
	
	# --------------------------------------------------------------------------
	# ------------------ Tk Widget Initialization START ------------------------
	def createHeader(self):
		'''
		Function that sets up the upper portion of the test application 
		(above "messagebox").

		@self: Required self argument.
		''' 
		self.header = Frame(self)
		self.header.pack({'fill':'both', 'expand':'true'})

		self.appLabel = Label(self.header)
		self.appLabel['text'] = self.testRunner.getTestInfo()['name']
		self.appLabel.pack({'padx':10, 'pady':10, 'fill':'x', 'expand':'false', 'side':'left'})

		self.licenseLabel = Label(self.header)
		self.licenseLabel['text'] = str('Author: ' + self.testRunner.getTestInfo()['author'])
		self.licenseLabel.pack({'padx':10, 'pady':10, 'fill':'x', 'expand':'false', 'side':'right'})

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


	def createWidgets(self):
		'''
		Function that instansiates the lower portion of the application text-
		box ("messagebox") and below.

		@self: Required self argument.
		''' 
		self.textBox = tkst.ScrolledText(
			master = self,
			wrap= WORD,
			width=100,
			height=30
		)

		self.textBox.pack(padx=10, pady=10, fill=BOTH, expand=True)
		defaultString = self.testRunner.getCurStateText()
		# self.textBox.insert(INSERT, defaultString)
		# self.textBox.tag_add("start","1.8","1.13")
		# self.textBox.tag_config("start", background="black",foreground="red")
		self.updateAndFormatTextBox(defaultString)

		style = ttk.Style() 
		style.configure('TButton', foreground="red") 
		style.map("TButton",
		  foreground=[('pressed', 'red'), ('active', 'red')],
		  background=[('pressed', '!disabled', 'black'),
					  ('active', 'white')]
		)

		self.runButton = tk.Button(self,width=20, height=2)
		self.runButton["text"] = "Run <F2>"
		self.runButton["command"] = self.startTest
		self.runButton.pack({"side": "left",'padx':10,'pady':10})

		self.QUIT = tk.Button(self, width=20, height=2)
		self.QUIT["text"] = "QUIT <F4>"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.quit
		self.QUIT.pack({"side": "right",'padx':10})

'''
Class that manages the threaded execution of a process.
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

'''
Define a function to be called externally that executes the application.
'''
def TestApplicationInit(testRunner):
	root = Tk()
	app = TestApplication(testRunner, master=root)
	app.mainloop()
	root.destroy()
	return {'root':root,'app':app}






''' Author(s): Chris Johnson (chrisjohn404) September 2020'''