'''
Colors (Implements "bcolors")
Author: Chris Johnson (chrisjohn404)
June 2022
License: GPLv2
 - Expose bcolors class and helper functions for CLI printing with colors.
'''
'''
0: normal brightness
1: bright/bold
2: dull/dark

3: Italic
4: Underline
5: ??
6: ??
7: Highlighted
8: ?? Off?
9: Struck-out (line through center)
21: Double Underline

~30-36 colors
~41-47: Highlights
~90-97: Bold Colors
~ 100-107: Bold Highlights

https://gist.github.com/jrjhealey/1eac73a1d1aa411990ab7bfd4a1687d9
https://wiki.tcl-lang.org/page/ANSI+color+control

'''
tclInterpretationCodes = {
	"0": {"color": 'normal', "fg": False, "bg": False, "style": True},
	"1": {"color": 'bold', "fg": False, "bg": False, "style": True},
	"2": {"color": 'dull', "fg": False, "bg": False, "style": True},
	"3": {"color": 'italic', "fg": False, "bg": False, "style": True},
	"4": {"color": 'underline', "fg": False, "bg": False, "style": True},
	"7": {"color": 'highlighted', "fg": False, "bg": False, "style": True},
	"9": {"color": 'struck-out', "fg": False, "bg": False, "style": True},
	"21": {"color": 'double-underline', "fg": False, "bg": False, "style": True},
	"30": {"color": 'black', "fg": True, "bg": False, "style": False},
	"31": {"color": 'red', "fg": True, "bg": False, "style": False},
	"32": {"color": 'green', "fg": True, "bg": False, "style": False},
	"33": {"color": 'yellow', "fg": True, "bg": False, "style": False},
	"34": {"color": 'blue', "fg": True, "bg": False, "style": False},
	"35": {"color": 'purple', "fg": True, "bg": False, "style": False},
	"36": {"color": 'cyan', "fg": True, "bg": False, "style": False},
	"37": {"color": 'white', "fg": True, "bg": False, "style": False},
	"40": {"color": 'black', "fg": False, "bg": True, "style": False},
	"41": {"color": 'red', "fg": False, "bg": True, "style": False},
	"42": {"color": 'green', "fg": False, "bg": True, "style": False},
	"43": {"color": 'yellow', "fg": False, "bg": True, "style": False},
	"44": {"color": 'blue', "fg": False, "bg": True, "style": False},
	"45": {"color": 'purple', "fg": False, "bg": True, "style": False},
	"46": {"color": 'cyan', "fg": False, "bg": True, "style": False},
	"47": {"color": 'white', "fg": False, "bg": True, "style": False},
	"90": {"color": 'black', "fg": True, "bg": False, "style": False},
	"91": {"color": 'red', "fg": True, "bg": False, "style": False},
	"92": {"color": 'green', "fg": True, "bg": False, "style": False},
	"93": {"color": 'yellow', "fg": True, "bg": False, "style": False},
	"94": {"color": 'blue', "fg": True, "bg": False, "style": False},
	"95": {"color": 'purple', "fg": True, "bg": False, "style": False},
	"96": {"color": 'cyan', "fg": True, "bg": False, "style": False},
	"97": {"color": 'white', "fg": True, "bg": False, "style": False},
	"100": {"color": 'black', "fg": False, "bg": True, "style": False},
	"101": {"color": 'red', "fg": False, "bg": True, "style": False},
	"102": {"color": 'green', "fg": False, "bg": True, "style": False},
	"103": {"color": 'yellow', "fg": False, "bg": True, "style": False},
	"104": {"color": 'blue', "fg": False, "bg": True, "style": False},
	"105": {"color": 'purple', "fg": False, "bg": True, "style": False},
	"106": {"color": 'cyan', "fg": False, "bg": True, "style": False},
	"107": {"color": 'white', "fg": False, "bg": True, "style": False},
}


class Codes:
	start = '\033['
	
	
	black = '30'
	alt_red = '31'
	alt_green = '32'
	alt_yellow = '33'
	alt_blue = '34'
	alt_purple = '35'
	alt_cayan = '36'
	alt_white = '37'

	grey = '90'
	red = '91'
	green = '92'
	yellow = '93'
	blue = '94'
	purple = '95'
	cyan = '96'
	white = '97'
	end = 'm'
	
class bcolors:
	HEADER = f'{Codes.start}95{Codes.end}'
	# OKBLUE = f'{Codes.start}94{Codes.end}'
	# OKCYAN = f'{Codes.start}96{Codes.end}'
	# OKGREEN = f'{Codes.start}92{Codes.end}'
	# WARNING = f'{Codes.start}93{Codes.end}'
	# FAIL = f'{Codes.start}91{Codes.end}'
	OKBLUE = f'{Codes.start}37;104{Codes.end}'
	OKCYAN = f'{Codes.start}37;106{Codes.end}'
	OKGREEN = f'{Codes.start}37;102{Codes.end}'
	WARNING = f'{Codes.start}37;103{Codes.end}'
	FAIL = f'{Codes.start}37;101{Codes.end}'
	ENDC = f'{Codes.start}0{Codes.end}'
	BOLD = f'{Codes.start}1{Codes.end}'
	ITALIC = f'{Codes.start}1{Codes.end}'
	UNDERLINE = f'{Codes.start}4{Codes.end}'

def color(color, s):
	return f'{bcolors[color]}s{bcolors.ENDC}'

def okStr(s):
	return color('OKBLUE', s)

def failStr(s):
	return color('FAIL', s)

def passStr(s):
	return color('OKGREEN', s)

def warnStr(s):
	return color('WARNING', s)

if __name__ == "__main__":
	print('Testing...')
	# Bold, Underline, Struck-out, Double Underline, test...
	for i in range(30,37):
		# print(f'\033[0;{i}m{i}:HELLO\033[0m')
		print(f'\033[1;4;9;21;{i}m{i}:HELLO\033[0m')
		# print(f'\033[2;{i}m{i}:HELLO\033[0m')
	for i in range(90,97):
		print(f'\033[1;4;9;21;{i}m{i}:HELLO\033[0m')
	for i in range(40,47):
		print(f'\033[1;4;9;21;{i}m{i}:HELLO\033[0m')
	for i in range(100,107):
		print(f'\033[1;4;9;21;{i}m{i}:HELLO\033[0m')
	
	print('\033[1;4;9;21;46;106mWORLD\033[0m')
	for i in range (0,9):
		for j in range (30,37):
			for k in range(40,47):
				print(f'\033[{i};{j};{k}m{i},{j},{k}\033[0m')
				print(f'\033[{i};{j};{k+60}m{i},{j},{k+60}\033[0m')
				print(f'\033[{i};{j+60};{k}m{i},{j+60},{k}\033[0m')
				print(f'\033[{i};{j+60};{k+60}m{i},{j+60},{k+60}\033[0m')



''' Author(s): Chris Johnson (chrisjohn404) June 2020'''