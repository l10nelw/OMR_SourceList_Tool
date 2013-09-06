"""
Renames Rpt%5FOnlineMediaReach.xls and creates new Source List excel file (Preparation phase)
Created: 2013-08-05
Modified: 2013-08-07
Author: lionel.wong@isentia.com

How to use:
Ensure "Rpt%5FOnlineMediaReach.xls" and "Source List template.xlsx" are in the same folder where this script is located
Run makesourcelist0.bat
"""

import calendar
from datetime import date, timedelta
import os
import shutil

OMRREPORT_NAME = { 'old': 'Rpt%5FOnlineMediaReach.xls', 'new': 'Rpt_OnlineMediaReach {}.xls' }
SOURCELIST_NAME = { 'old': 'Source List template.xlsx', 'new': 'Source List {}.xlsx' }

def addmonth(d, n):
	"Add n months (can be negative) to date d, ignoring day"
	d = date(d.year, d.month, 15) # middle of the month for addition safety
	if n == 0:
		return d
	else:
		plusminus1 = int(abs(n)/n)
		return addmonth(d + timedelta(days=30*plusminus1), n - plusminus1)

def monthnames(datelist):
	"""
	Turn list of dates into string series of MMM month names and YYYY year at the end of each yearly series
	E.g. 2012-11-1, 2012-12-04, 2013-01-18, 2013-02-28, 2013-03-09 > Nov Dec 2012 Jan Feb Mar 2013
	"""
	words = []
	years = set()
	for d in datelist:
		words.append(calendar.month_abbr[d.month])
		words.append(str(d.year))
	words.reverse()
	for i, w in enumerate(words):
		if len(w) == 4: # is year
			if w in years:
				del words[i]
			else:
				years.add(w)
	words.reverse()
	return words

def fileop(op, filename, monthseries):
	"""
	Perform operation (op) on a file (filename) with a formatted list of dates (monthseries) added to new name
	Operation choices are: os.rename, shutil.copy
	"""
	opname = op.__name__ + ':'
	old = filename['old']
	new = filename['new'].format(' '.join(monthnames(monthseries)))
	print(opname, old, '>', new)
	try:
		if os.path.isfile(new): raise OSError
		op(old, new)
	except FileNotFoundError: print(old, 'not found.')
	except OSError: print(new, 'already exists.')
#

def main():

	monthseries = [addmonth(date.today(), i) for i in (0, 1, -3, -2, -1)] # thismonth next1month last3month last2month last1month
	fileop(os.rename, OMRREPORT_NAME, monthseries[-3:]) # last 3 months
	fileop(shutil.copy, SOURCELIST_NAME, monthseries[:2]) # this and next month
	
if __name__=='__main__': main()