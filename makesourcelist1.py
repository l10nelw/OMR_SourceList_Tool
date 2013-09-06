"""
Generate source list - phase 1
Created: 2013-06-16 / Modified: 2013-08-09
Author: lionel.wong@isentia.com

How this works:
Input: data.txt
Performs the following:
- removes duplicate entries
- replaces entries specified in to-replace.txt
- removes entries without names (blanks)
- removes entries with illegal characters
- removes entries specified in to-remove.txt
- removes entries with names specified in obsolete-web.txt and obsolete-ugc.txt
- removes entries without WEB/UGC prefixes (no type)
Output: FILTERED.TXT

data.txt:
Original data taken from Rpt_OnlineMediaReach...xls

to-remove.txt:
List entries you want to remove, e.g. duplicate sources with different/misspelled names

to-replace.txt:
List entries you want to replace, e.g. missing WEB/UGC prefix, misspelled names
Place new replacement-entry after each corresponding old entry-to-replace

obsolete-web.txt, obsolete-ugc.txt:
Obsolete entries taken from "Obsolete publications.xlsx" separated according to WEB/UGC
Entries are checked by name only

How to use:
Run makesourcelist1.bat

If makesourcelist1.py is run on its own, removed entries and counts will be displayed but not saved to REMOVED.TXT
"""

from makesourcelist_ import *

# filter parameters:

BLANK_LIST = ['', '.', '_']
ILLEGAL_LIST = r'\/:;*?"|<>'
TOREMOVE_LIST = read_file('to-remove.txt')
TOREPLACE_LIST = read_replacefile('to-replace.txt')
OBSOLETE_LIST = { 'WEB': read_file('obsolete-web.txt'), 'UGC': read_file('obsolete-ugc.txt') }

# filter tests:

def is_toreplace(entry):
	try:
		return TOREPLACE_LIST[entry]
	except KeyError:
		return False

def is_blank(entry):
	return entry.name in BLANK_LIST

def is_illegal(entry):
	for char in entry.name:
		if char in ILLEGAL_LIST: return True
	return False

def is_toremove(entry):
	return entry in TOREMOVE_LIST

def is_obsolete(entry):
	try:
		for x in OBSOLETE_LIST[entry.type]:
			if entry.name == x.name: return True
	except KeyError: pass
	return False

def is_notype(entry):
	return entry.type is ''

"""
Series of filter functions
Filters apply left-to-right in order of descending expected frequency, except replace always before remove
If one filter hits, remaining ones are skipped
"""
FILTERS = (is_toreplace, is_blank, is_illegal, is_toremove, is_obsolete, is_notype)

####### phase 1 #######

def main():

	def print_action(entry, filtername):
		print(	filtername+':',
				entry.type,
				entry.name.encode('ascii', 'ignore').decode(),
				entry.link,
				entry.country )
		count[filtername] += 1

	counters = ['original', 'duplicate'] + [f.__name__[3:] for f in FILTERS] + ['remainder']  # f.__name__[3:] removes 'is_'
	count = dict([(counter, 0) for counter in counters])

	data = read_file('data.txt')
	count['original'] = len(data)

	data = set(data)
	count['duplicate'] = count['original'] - len(data)

	print('Phase 1...')

	filtered = []
	for entry in data:
		for f in FILTERS: # run entry though filters
			hit = f(entry)
			if hit:
				if isinstance(hit, Entry1): filtered.append(hit) # if hit contains replacement entry, use it
				print_action(entry, f.__name__[3:])
				break # skip remaining filters, go to next entry
		else:
			filtered.append(entry) # passed through all filters

	write_file('FILTERED.TXT', filtered)
	count['remainder'] = len(filtered)
	print('duplicates are not listed')
	print()
	for c in counters:
		action = 'replaced' if c=='toreplace' else 'removed'
		action = '' if c in ('original', 'remainder') else action
		print(count[c], c, action)

if __name__=='__main__': main()
