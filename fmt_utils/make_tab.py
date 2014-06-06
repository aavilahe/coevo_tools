#!/usr/bin/env python
''' make_tab.py -- formats output of coevolution programs

	Steps:
		1. Whitespace (or comma for plmDCA) to tab '\t'
		2. Left, Right positions in first, second columns respectively
		3. Keep only inter-protein pairs
		4. Re-number concatenated aln to match split alns
		5. Make numberings start at 0
		6. Add dummy p-values

'''

import sys

def is_int(str_list):
	''' Checks if each element in str_list represents an int

	'''

	try:
		for s in str_list:
			int(s)
	except ValueError:
		return False
	return True

def read_output(fh, fmt):
	''' Read file and return lines as list of list of fields
		
		Make column numbering start at **one**

	'''

	if fmt == 'plmDCA':
		delim = ','
	else:
		# whitespace
		delim = None
	
	if fmt in ('plmDCA', 'mfDCA', 'psicov', 'hpDCA'):
		OFFSET=1
	else:
		OFFSET=0
	
	lines = [ line.strip().split(delim) for line in fh.readlines() ]

	oned_lines = list()

	for line in lines:
		if len(line) >= 3 and is_int(line[:2]):
			pos1, pos2  = map(int, line[:2])
			pos1 += 1 - OFFSET
			pos2 += 1 - OFFSET
			oned_lines += [ [pos1, pos2] + line[2:] ]
#		else:
#			print '\t'.join(line)
	return oned_lines

def remove_extra_stuff(lines, fmt):
	''' remove unecessary columns from lines

	'''

	cln_lines = list()

	for line in lines:
		if fmt == 'psicov':
			# pos1, pos2, psicov score
			cln_lines += [[ line[i] for i in (0,1,4) ]]
		elif fmt == 'mfDCA':
			# pos1, pos2, mut inf, dca
			cln_lines += [[ line[i] for i in (0,1,2,3) ]]
		elif fmt == 'plmDCA':
			# pos1, pos2, frob norm dca
			cln_lines += [[ line[i] for i in (0,1,2) ]]
		else:
			# infCalc
			# pos1, pos2, h1, h2, hj, mi, vi, zminmi, zjmi
			# hpDCA
			# pos1, pos2, hpdca
			cln_lines += [ line ]
	
	return cln_lines

def keep_interProtein(lines, last_left):
	''' returns a copy of lines with only inter-protein pairs

	'''
	
	keep_lines = list()

	for line in lines:
		pos1, pos2 = sorted(line[:2])
		if pos1 <= last_left and pos2 > last_left:
			keep_lines += [ [ pos1, pos2 ] + line[2:] ]
	
	return keep_lines

def renumber_positions(lines, last_left):
	''' returns a copy of lines with renumbered positions to match split aln

	'''
	
	renum_lines = list()
	
	for line in lines:
		pos1, pos2 = line[:2]

		if pos1 > last_left:
			pos1 -= last_left
		if pos2 > last_left:
			pos2 -= last_left

		renum_lines += [ [ pos1, pos2 ] + line[2:] ]
	
	return renum_lines

def make_zero_index(lines):
	''' make column numbering start at **zero** instead of **one**

	'''

	zeroed_lines = list()

	for line in lines:
		pos1, pos2 = line[:2]
		pos1 -= 1
		pos2 -= 1
		
		zeroed_lines += [ [ pos1, pos2 ] + line[2:] ]
	
	return zeroed_lines

def add_dummy_pvalues(lines, fmt):
	''' TEMPORARY HACK: add dummy p-value columns

	'''

	print >>sys.stderr, "temporarily hacking dummy p-values"

	lines_w_pvals = list()

	#num_cols_to_add = len(lines[0]) - 2
	if fmt == 'infCalc':
		num_cols_to_add = 4
	elif fmt == 'mfDCA':
		num_cols_to_add = 2
	else:
		# psicov, plmDCA, hpDCA
		num_cols_to_add = 1

	for line in lines:
		lines_w_pvals += [ line + [ 'nan' ]*num_cols_to_add ] 			
	
	return lines_w_pvals

if __name__ == '__main__': 
	usage=(
			"usage: %s fmt last_left < output > output_tab\n"+
			" fmt: mfDCA, plmDCA, hpDCA, psicov, infCalc\n"+
			" last_left: last aln col of left protein. one based"
	) % sys.argv[0]
	if len(sys.argv) not in (2,3):
		exit(usage)
	
	fmt = sys.argv[1]
	last_left = int(sys.argv[2])
	if fmt not in ("mfDCA", "plmDCA", "psicov", "infCalc", "hpDCA"):
		print >>sys.stderr, "Warning!: unrecognized format [ %s ]" % fmt
	
	the_lines = read_output(sys.stdin, fmt)
	the_lines = remove_extra_stuff(the_lines, fmt)
	if fmt != 'infCalc':
		# infCalc format is already correctly numbered and filtered
		# BUT read_output() has one-indexed it!
		the_lines = keep_interProtein(the_lines, last_left)
		the_lines = renumber_positions(the_lines, last_left)
	the_lines = make_zero_index(the_lines) # zero-index all fmts
	the_lines = add_dummy_pvalues(the_lines, fmt)

	for line in the_lines:
		print '\t'.join(map(str, line))
	

