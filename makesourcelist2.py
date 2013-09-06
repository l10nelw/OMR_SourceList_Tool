"""
Generate source list - phase 2
Created: 2013-06-17 / Modified: 2013-08-09
Author: lionel.wong@isentia.com

How this works:
Input: FILTERED.TXT
Performs the following:
- Segregates entries by country
- Removes duplicates in each country set
- Sorts each set by name, then country, then type
Output: LIST [COUNTRY].TXT

How to use:
Run makesourcelist2.bat

If makesourcelist2.py is run on its own, duplicate count will be displayed but not saved to REMOVED.TXT
"""

from makesourcelist_ import *
from operator import attrgetter

COUNTRIES = ['AUSTRALIA', 'NEW ZEALAND', 'MALAYSIA', 'SINGAPORE', 'CHINA', 'HONG KONG', 'INTERNATIONAL']
COUNTRYRENAME = { 'UNASSIGNED':'INTERNATIONAL', 'VIET NAM':'VIETNAM' }

####### phase 2 #######

def main():

	filtered = read_file('FILTERED.TXT', typed=True)
	count_start = count_dupes = len(filtered)

	segregated = dict()
	for country in COUNTRIES: segregated[country] = set() # sets remove duplicates

	# segregate
	for entry in filtered:
		country = entry.country
		if country in COUNTRYRENAME: country = COUNTRYRENAME[country]
		entry = Entry2(TYPE[entry.type], entry.name, country) # rename type (WEB/UGC to News/Blogs), remove entry.link
		if country in segregated:
			segregated[country].add(entry)
		else:
			segregated['INTERNATIONAL'].add(entry)

	# sort
	for country in segregated:
		segregated[country] = list(segregated[country]) # turn sets into sortable lists
		segregated[country].sort(key=attrgetter('name'))
		segregated[country].sort(key=attrgetter('country'))
		segregated[country].sort(key=attrgetter('type'), reverse=True)
		write_file('LIST '+country+'.TXT', segregated[country]) # output country .txt files
		count_dupes -= len(segregated[country])

	print()
	print('Phase 2...')
	print(count_dupes, 'duplicate removed')
	print(count_start - count_dupes, 'remainder')

if __name__=='__main__': main()