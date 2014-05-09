#!/usr/bin/env python
''' concatenate_fastas.py -- concatenate corresponding sequences in two fastas

	seqids must be exact and unique within each fasta

'''

import sys
import re

def ReadFasta(fh):
	''' Reads fasta file and returns alignment as a dict.
	
	'''

	ali = dict()
	header = ''
	seq = ''

	for line in fh:
		line = line.rstrip('\n\r')
		if line == '':
			continue
		if line.startswith('>'):
			if header != '':
				ali[header] =  re.sub('\s+', '',seq) 
				seq = ''
			header = line
			continue
		seq += line
	ali[header] =  re.sub('\s+', '',seq) 
	return ali

if __name__ == "__main__":
	if len(sys.argv) != 3:
		sys.exit('usage: %s left.fa right.fa > left_right.fa'%sys.argv[0])
	
	left_ali = ReadFasta(open(sys.argv[1], 'r'))
	right_ali = ReadFasta(open(sys.argv[2], 'r'))
	
	for seq_id, left_seq in left_ali.iteritems():
		if seq_id in right_ali:
			right_seq = right_ali[seq_id]
			print seq_id
			print left_seq
			print right_seq
		else:
			print >>sys.stderr, 'skipping %s' % seq_id


	


