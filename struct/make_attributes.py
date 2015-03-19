#!/usr/bin/env python
''' make_attributes.py -- converts co-evolution scores to attributes file

'''

import sys

def read_colmap(fh):
	''' read column to resnum map, return dict.
	
	'''

	return dict([ line.split()[:2] for line in fh.readlines() ])

def read_results(fh):
	''' read results, return (list of column names, list of rows of columns)

	'''

	lines = fh.readlines()

	ColumnNames = lines[0].split()
	
	Rows = [ line.split() for line in lines[1:] ]

	return (ColumnNames, Rows)


def make_attributes(ColToResNum, ColNames, Rows):
	''' print attribute control and assignment lines (atom-spec and score)
	
	'''

	for i,colName in enumerate(ColNames[1:], 1):
		print 'attribute: %s' % colName
		print 'match mode: 1-to-1'
		print 'recipient: residues'
		for cols in Rows:
			ColCoord = cols[0]
			if ColCoord in ColToResNum:
				resnum = ColToResNum[ColCoord]
				attr_val = cols[i]
				print '\t:%s\t%s' % (resnum, attr_val)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print >>sys.stderr, 'usage: %s results.tab colresnum.map > attributes.txt' % sys.argv[0]
		sys.exit(1)
	
	results = open(sys.argv[1], 'r')
	colmap = open(sys.argv[2], 'r')

	ColNames, Rows = read_results(results)
	ColToResNum = read_colmap(colmap)
	make_attributes(ColToResNum, ColNames, Rows)


