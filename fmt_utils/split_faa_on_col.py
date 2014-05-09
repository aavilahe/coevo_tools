#!/usr/bin/env python
''' split_faa_on_col.py -- split an aligned fasta on columns

	Splits an alignment on a specified column.

	Writes two fasta files.
	Does not modify seq order.
	Appends '_L|R' to seq identifier; comment is included but left alone

'''

import sys
import re

def ReadFasta(fh):
	''' Reads fasta file and returns alignment as a list of tuples
	
	'''

	ali = list()
	header = ''
	seq = ''

	for line in fh:
		line = line.rstrip('\n\r')
		if line == '':
			continue
		if line.startswith('>'):
			if header != '':
				ali += [ (header, re.sub('\s+', '',seq)) ]
				seq = ''
			header = line
			continue
		seq += line
	ali += [ (header, re.sub('\s+','',seq)) ]
	return ali

def splitAln(ali, nth_col):
	''' For each sequence in ali, split using nth_col.
		
		col: 1,2,3,...,N,N+1,...,K
		      <--Left--| |--Right-->

	'''

	left_ali = list() # [ (header,seq), (header,seq), ... ]
	right_ali = list()
	for (header, sequence) in ali:
		split_header= header.split()
		ident, comment = split_header[0], ' '.join(split_header[1:])
		left_header = ("%s_L %s" % (ident, comment)).strip()
		right_header = ("%s_R %s" % (ident, comment)).strip()
		
		left_seq = sequence[:nth_col]
		right_seq = sequence[nth_col:]

		left_ali += [(left_header, left_seq)]
		right_ali += [(right_header, right_seq)]
	return left_ali,right_ali

def printAlns(left_ali, right_ali, LEFTOUT, RIGHTOUT):
	''' Print left and right sequences to two fastas.

	'''

	for (idx, (header, seq)) in enumerate(left_ali):
		print >>LEFTOUT, header
		print >>RIGHTOUT, right_ali[idx][0] #right_ali header
		print >>LEFTOUT, seq
		print >>RIGHTOUT, right_ali[idx][1] #right_ali sequence 

if __name__ == '__main__':
	if len(sys.argv) != 5:
		print >>sys.stderr, 'usage: %s ali.fa nth_col left.fa right.fa' % sys.argv[0]
		sys.exit(1)
	alifn = sys.argv[1]
	nth_col = int(sys.argv[2])
	leftfn = sys.argv[3]
	rightfn = sys.argv[4]

	ali = ReadFasta(open(alifn, 'r'))
	left_ali, right_ali = splitAln(ali, nth_col)
	printAlns(left_ali, right_ali, open(leftfn, 'w'), open(rightfn, 'w'))
	



