#!/usr/bin/env python
''' map column to pdb resnum '''

import sys
import getopt
import re
import tempfile
from os import remove
from subprocess import *

ALIGNER_AND_OPTIONS = 'msaprobs -num_threads 12 %s' # %s is the input filename

def getopts(args):
	''' Parse command line for options and return a dict.
		
		using getopt for compatibility
	
	'''

	optlist, args = getopt.getopt(args, 'h', ['help'])
	options = dict()
	usage = (
				'usage: %s [ -h | --help ] seqID align.phy chain.map \n'
			) % sys.argv[0]
	
	# Read command line
	for opt, val in optlist:
		if opt in ('-h', '--help'):
			sys.exit(usage)

	if len(args) != 3:
		print >>sys.stderr, 'wrong number of arguments'
		sys.exit(usage)

	options['refID'] = args[0].strip()
	options['align_fn'] = args[1]
	options['chain_fn'] = args[2]

	return options

def read_phy(fh):
	''' reads phylip file and returns a dict.
		
		strict format: first 10 chars for seqid, one sequence per line

	'''

	lines = fh.readlines()[1:]
	aln = dict([ (line[:10].strip(), re.sub('\s+', '', line[10:])) for line in lines ])

	return aln

def read_fa(fh):
	''' reads a fasta file and returns a dict

		'>' not included in seqID, comment is lost

	'''

	ali = list() # list of tuples
	seqID = ''
	seq = ''

	for line in fh:
		line = line.strip()
		if line == '':
			continue
		if line.startswith('>'):
			if seqID != '':
				ali += [(seqID, re.sub('\s+', '', seq))]
				seq = ''
			seqID = line[1:].split()[0] # split id line on whitespace, lose comment
			continue
		seq += line
	ali += [(seqID, re.sub('\s+', '', seq))] # remove whitespace from seqs

	ali = dict(ali)

	return ali

def read_chainMap(fh):
	''' reads tabular file, returns (list of ints, sequence)

	'''

	resNums = list()
	chainSeq = ''
	for line in fh:
		resnum, aa = line.split()
		resNums.append(int(resnum))
		chainSeq += aa
	
	return (resNums, chainSeq)
	

def make_ref2col(aln_ref):
	''' makes a map of column to refID position, returns generator of tuples

	'''

	# '-' is the only gap char allowed
	ref_col = enumerate(( i for i,aa in enumerate(aln_ref) if aa != '-' ), 1)
	return ref_col

def make_ref2pdbseq(refID, refSeq, chainID, chainSeq):
	''' makes a map from refSeq to chainSeq positions, returns generator of tuples

		generates a temp fasta file containing the two sequences
		calls an aligner and then maps the ungapped positions to each other

	'''

	tmpfh = tempfile.NamedTemporaryFile(suffix='.fa', delete=False)
	tmpfn = tmpfh.name

	print >>sys.stderr, 'creating temporary fasta < %s >' % tmpfn

	print >>tmpfh, '>%s\n%s\n>%s\n%s\n' % (refID, refSeq, chainID, chainSeq)
	tmpfh.close()

	aln_results = Popen( (ALIGNER_AND_OPTIONS % tmpfn).split(), stdout=PIPE ).communicate()[0] # keep stdout

	remove(tmpfn)

	aln = read_fa(aln_results.split('\n')) # read_fa works with a list of lines, too

	ref_tmpcol = make_ref2col(aln[refID])
	chain_tmpcol = make_ref2col(aln[chainID])
	chain_at_tmpcol = dict(((tmpcol, chain) for chain, tmpcol in chain_tmpcol))

	ref2pdbseq = ((ref, chain_at_tmpcol[tmpcol]) for (ref, tmpcol) in ref_tmpcol if tmpcol in chain_at_tmpcol)

	return ref2pdbseq

def make_pdbseq2resnum(resNums):
	''' makes a map from resnum to pdbseq, returns generator of tuples

	'''

	return enumerate(resNums, 1)

if __name__ == "__main__":
	options = getopts(sys.argv[1:])
	print >>sys.stderr, options

	phy_aln = read_phy(open(options['align_fn'], 'r'))

	refSeq = phy_aln[options['refID']]
	resNums, chainSeq = read_chainMap(open(options['chain_fn'], 'r'))

	ref2col = make_ref2col(refSeq)
	ref2pdbseq = dict(make_ref2pdbseq(options['refID'], refSeq, 'pdb_chain', chainSeq))
	pdbseq2resnum = dict(make_pdbseq2resnum(resNums))

	for ref, col in sorted(ref2col):
		if ref in ref2pdbseq:
			pdbseq = ref2pdbseq[ref]
			if pdbseq in pdbseq2resnum:
				resnum = pdbseq2resnum[pdbseq]
				print '%d\t%d' % (col, resnum)
				#print '%d\t%d\t%d\t%d' % (col, ref, pdbseq, resnum)

