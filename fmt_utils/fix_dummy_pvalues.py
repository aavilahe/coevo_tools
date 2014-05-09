#!/usr/bin/env python
''' reads observed tab and sim tabs calculates and attaches p-values to observed tab

'''

import sys
from math import isnan

def read_tab(fh, fields_to_keep):
	''' split each line into fields, save in dict

		fields_to_keep starts after left_col/right_col

		eg.
		left right stat stat stat dummyp dummyp dummyp
		0    1     2    3    4    5      6      7      <-raw idx
		-    -     0    1    2    3      4      8      <-fields_to_keep/to_comp idx

	'''
	
	tab = dict()
	for line in fh:
		fields = line.strip().split()
		left_col, right_col = tuple(fields[:2])
		the_line = [ float(fields[keep+2]) for keep in fields_to_keep ]
		tab[(left_col, right_col)] = the_line
	return tab

def count_pvals(fh, tab, fields_to_keep, fields_to_comp, fmt):
	''' lines from cat simtabs. split each line into fields, compare sim stats to obs stats

	'''

	ptab = dict()
	for line in fh:
		fields = line.strip().split()
		left_col, right_col = tuple(fields[:2])
		
		if (left_col, right_col) not in tab:
			# only count pvals for existing observed entries
			continue
		if (left_col, right_col) not in ptab:
			# initialize pval counter
			ptab[(left_col, right_col)] = [ 0 for sidx in fields_to_comp ]

		the_line = [ float(fields[keep+2]) for keep in fields_to_keep ]
		for pidx, sidx in enumerate(fields_to_comp):
			stat = the_line[sidx]
			obs_stat = tab[(left_col, right_col)][sidx]
			if fmt == 'infCalc' and sidx == 1:
				# VarInf is a distance (lower is better)
				if stat <= obs_stat:
					ptab[(left_col, right_col)][pidx] += 1
			else:
				if stat >= obs_stat:
					ptab[(left_col, right_col)][pidx] += 1
	return ptab

if __name__ == "__main__":
	if len(sys.argv) != 4:
		sys.exit(("usage: %s tabfmt ntabs <(cat *-sims/*_tab) < obs.tab > tab\n" +\
				"\ttabfmt: infCalc, mfDCA, psicov/hpDCA/plmDCA\n" +\
				"\tntabs: number of simulations (1000)") % sys.argv[0])
	tabfmt = sys.argv[1]
	ntabs = int(sys.argv[2])
	simtabs_fh = open(sys.argv[3], 'r')
	
	if tabfmt == 'infCalc':
		# don't calculate p-values for entropies
		fields_to_keep = range(7) # 0-6 lh rh jh mi vi mi/minh mi/jh
		fields_to_comp = range(3,7) # 3-6 mi vi mi/minh mi/jh
	elif tabfmt == 'mfDCA':
		fields_to_keep = range(2) # 0,1 mi dca
		fields_to_comp = range(2)
	else:
		fields_to_keep = range(1) # 0 psicov/whatev
		fields_to_comp = range(1)
	
	tab = read_tab(sys.stdin, fields_to_keep)

	ptab = count_pvals(simtabs_fh, tab, fields_to_keep, fields_to_comp, tabfmt)

	pinc = 1.0 / ntabs

	for coords, line in tab.iteritems():
		if coords in ptab:
			pline = [ ("%.6f" % (p * pinc)) for p in ptab[coords] ]
		else:
			pline = [ 0.000 for sidx in fields_to_comp ]
		# set pvals to 1 for stats == 'nan'
		for pidx, sidx in enumerate(fields_to_comp):
			if isnan(tab[coords][sidx]):
				pline[pidx] = 1.0
		the_line = '\t'.join(map(str, list(coords) + list(line) + list(pline)))
		print the_line


