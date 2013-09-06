"""
Module of common objects for makesourcelist1.py and makesourcelist2.py
Created: 2013-06-17 / Modified: 2013-08-09
Author: lionel.wong@isentia.com
"""

import collections

Entry1 = collections.namedtuple('Entry1', 'type name link country') # phase 1
Entry2 = collections.namedtuple('Entry2', 'type name country') # phase 2

TYPE = { 'WEB': 'News', 'UGC': 'Blogs' }

def read_line(entry, typed=False):
	entry = entry.split('\t')
	entry = [item.strip() for item in entry]
	
	link = entry[-2]
	if not link.startswith(('http://','https://')):
		entry[-2] = 'http://' + link
		
	entry[-1] = entry[-1].upper() # country
	
	if typed:
		entry = Entry1(*entry)
	else:
		# split type prefix from name
		type = entry[0][:3]
		if type in TYPE:
			entry[0] = entry[0][4:]
		else:
			type = ''
		entry = Entry1(type, *entry)
	
	return entry

def read_file(filename, typed=False):
	data = []
	with open(filename, 'r') as f:
		while True:
			entry = f.readline()
			if entry is '\n': continue # ignore blank lines
			if not entry: break # end of file
			data.append(read_line(entry, typed))
	return data

def read_replacefile(filename):
	"Turn 'AB AB AB' string into {A:B,A:B,A:B} dict"
	file = read_file(filename)
	n = len(file)
	return { file[line]:file[line+1] for line in range(0, n - n%2, 2) }
	# -n%2 (remainder of n/2) so that only pairs of lines are read, any lone last line is ignored

def write_file(filename, data):
	with open(filename, 'w') as f:
		for entry in data:
			f.write('\t'.join(entry) + '\n')
