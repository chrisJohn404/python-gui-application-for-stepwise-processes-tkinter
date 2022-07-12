'''
Colors (Implements "bcolors")
Author: Chris Johnson (chrisjohn404)
June 2022
License: GPLv2
 - Expose bcolors class and helper functions for CLI printing with colors.
'''

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






''' Author(s): Chris Johnson (chrisjohn404) June 2020'''