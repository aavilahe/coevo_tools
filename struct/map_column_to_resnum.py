#!/usr/bin/env python
''' map_column_to_resnum.py -- map alignment column to resnum in pdb chain
	
	Example: chain A in 3DGE starts at 246, but alignment covers discontinuous domains

'''

import sys
import getopt
import re
import tempfile
import gzip
from os import remove
from os.path import basename
from subprocess import *
import Bio.PDB
import Bio.SeqUtils

__author__ = "Aram Avila-Herrera"

PROFILE_ALN_AND_OPTIONS = 'fmuscle -profile -in1 %s -in2 %s -out /dev/stdout'
PAIRWISE_ALN_AND_OPTIONS = 'needle -auto -asequence %s -bsequence %s -stdout -aformat3 fasta'

def parseCommandLine(args):
	''' Parse command line for options and return a dict.
		
		using getopt for compatibility
	
	'''

	optlist, args = getopt.getopt(args, 'hr:', ['help', 'refid='])
	options = dict()
	usage = (
				'usage: %s [ options ] chain_id pdb_file aln.fa\n\n' +\
				'Options:\n' +\
				'-h, --help           print this help and exit\n' +\
				'-r, --refid REFID    map using given reference seq id in alignment\n\n'
			) % sys.argv[0]
	
	# Read command line
	for opt, val in optlist:
		if opt in ('-h', '--help'):
			sys.exit(usage)
		if opt in ('-r', '--refid'):
			options['refid'] = val

	if len(args) != 3:
		print >>sys.stderr, 'wrong number of arguments'
		sys.exit(usage)

	options['chain_id'] = args[0]
	options['pdb_file'] = args[1]
	options['aln.fa'] = args[2]

	return options

def readFasta(fh):
	''' reads a fasta file (or list of lines) and returns a dict

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

def alignWrap(CMD_TEMPLATE, fa1, fa2):
	''' wrapper aligns sequences in two given fasta files

		returns dict: key = seqid, value = seq

	'''
	
	cmd = (CMD_TEMPLATE % (fa1, fa2)).split()
	profile_alignment = Popen(cmd, stdout=PIPE).communicate()[0] # watch out for large alignments
	ali_dict = readFasta(profile_alignment.split('\n')) # parse

	return ali_dict

def openModel(pdb_fn):
	''' opens first model in given pdb file name

		if file name ends in .gz, will attempt to open as a gzipped file

	'''

	if pdb_fn.endswith('.gz'):
		pdb_fh = gzip.open(pdb_fn)
	else:
		pdb_fh = open(pdb_fn)

	pdb_id = basename(pdb_fn).split('.')[0]
	structure = Bio.PDB.PDBParser().get_structure(pdb_id, pdb_fh)
	model = structure[0] # assume 1 model in pdb file
	
	return model

def getNonHetResidues(chain):
	''' get list of residues from chain, remove those with het flag

	'''

	all_res = chain.get_residues()
	nonhet_res = [ res for res in all_res if res.get_id()[0] == ' ' ]
	return nonhet_res

def chainToFasta(chain_id, nonhet):
	''' returns fasta string of chain sequence

	'''

	fasta_str = '>%s\n' % chain_id
	fasta_str += ''.join(( Bio.SeqUtils.seq1(res.resname) for res in nonhet ))
	return fasta_str

def makeTempFasta(fasta_str):
	''' make temporary fasta file

	'''

	tmp_fh = tempfile.NamedTemporaryFile(suffix='.fa', delete=False)
	print >>tmp_fh, fasta_str
	print >>sys.stderr, 'Created temporary fasta "%s"' % tmp_fh.name
	tmp_fh.close()

	return tmp_fh

def trimAln(og_aln, pr_aln):
	''' remove pr_aln columns not in og_aln

	'''

	og_len = len(og_aln.itervalues().next())
	pr_len = len(pr_aln.itervalues().next())

	# pr alignment with only sequences in og alignment
	pr_subaln = dict(( (seqid, seq) for (seqid, seq) in pr_aln.iteritems() if seqid in og_aln ))

	pr_curr = 0
	fin_idx_set = set()
	for og_idx in xrange(og_len):
		# find a match for each og column
		og_col = getCol(og_aln, og_idx)
		for pr_idx in xrange(pr_curr, pr_len):
			# search all pr columns starting at pr_curr
			pr_subcol = getCol(pr_subaln, pr_idx)
			if isSameColumn(og_col, pr_subcol):
				fin_idx_set.add(pr_idx)
				pr_curr = pr_idx + 1
				break
	
	if len(fin_idx_set) != og_len:
		print >>sys.stderr, 'Warning: profile alignment messed up original alignment columns!'
	
	trim_aln = dict(( (seqid, getAAs(seq, fin_idx_set)) for (seqid, seq) in pr_aln.iteritems() ))

	return trim_aln

def getAAs(seq, idxs):
	''' get amino acids at given indices

		return string of amino acids or list of other elements

	'''
	
	subseq = [ aa for (idx, aa) in enumerate(seq) if idx in idxs ]
	if all(( (isinstance(aa, basestring) and len(aa) == 1) for aa in subseq )):
		subseq = ''.join(subseq)
	
	return subseq

def getCol(aln, idx):
	''' get column idx of aln

	'''

	seqid_aa = dict(( (seqid, seq[idx]) for (seqid, seq) in aln.iteritems() ))

	return seqid_aa

def isSameColumn(colA, colB):
	''' test if two columns (dictionaries) are the same, seqs (keys) may be in any order

		requires same number of sequences in both columns for equality

	'''

	return set(colA.items()) == set(colB.items())

def getElementAlongSeq(aln_seq, el):
	''' inserts gaps from aln_seq into element_list

	'''

	# reverse element_list
	rel = el[::-1]
	place_elements = lambda aa: '-' if aa == '-' else rel.pop()
	eleAlongSeq = [ place_elements(aa) for aa in aln_seq ]

	return eleAlongSeq

def alignChainToAln(aln_fn, chain_id, nonhet_chain):
	''' align residues in nonhet_chain to alignment in aln_fn

		return (col, resnum, aa)

	'''

	# profile align alignment and pdb chain
	og_aln = readFasta(open(aln_fn))

	chain_fa_str = chainToFasta(chain_id, nonhet_chain)
	tmp_chain_fa_fh = makeTempFasta(chain_fa_str)

	pr_aln = alignWrap(PROFILE_ALN_AND_OPTIONS, aln_fn, tmp_chain_fa_fh.name)
	remove(tmp_chain_fa_fh.name)

	# add resnum and trim pr_aln
	resnums = [ res.get_id()[1] for res in nonhet_chain ]
	pr_aln_resnums = getElementAlongSeq(pr_aln[chain_id], resnums)

	pr_aln['_RESNUM_'] = pr_aln_resnums
	tr_aln = trimAln(og_aln, pr_aln)

	col_resnum_aa = [ (col, resnum, tr_aln[chain_id][col]) for (col, resnum) in enumerate(tr_aln['_RESNUM_']) if resnum != '-' ]

	return col_resnum_aa

def alignChainToRefId(ref_id, aln_fn, chain_id, nonhet_chain):
	''' align residues in nonhet_chain to alignment in aln_fn through a reference sequence

		return (col, resnum, aa)
	
	'''
	

	# align ref seq and pdb chain
	og_aln = readFasta(open(aln_fn))
	ref_seq = og_aln[ref_id]

	chain_fa_str = chainToFasta(chain_id, nonhet_chain)
	tmp_chain_fa_fh = makeTempFasta(chain_fa_str)

	refseq_fa_str = '>%s\n%s' % (ref_id, ref_seq)
	tmp_refseq_fa_fh = makeTempFasta(refseq_fa_str)

	pa_aln = alignWrap(PAIRWISE_ALN_AND_OPTIONS, tmp_refseq_fa_fh.name, tmp_chain_fa_fh.name)
	remove(tmp_chain_fa_fh.name)
	remove(tmp_refseq_fa_fh.name)
	
	# add resnum
	resnums = [ res.get_id()[1] for res in nonhet_chain ]
	pa_aln_resnums = getElementAlongSeq(pa_aln[chain_id], resnums)

	# map column to refseq position in original alignment
	# map refseq position to column in pairwise alignment
	# map pairwise column to resnum, aa

	ref_seq_len = len(ref_seq.replace('-',''))
	refpos_list = range(1, ref_seq_len + 1)
	og_aln_refpos = getElementAlongSeq(ref_seq, refpos_list)
	pa_aln_refpos = getElementAlongSeq(pa_aln[ref_id], refpos_list)

	pacolATrefpos = dict(( (refpos, pacol) for (pacol, refpos) in enumerate(pa_aln_refpos) ))
	col_pacol = ( (col, pacolATrefpos[refpos]) for (col, refpos) in enumerate(og_aln_refpos) if refpos != '-' )
	col_resnum_aa = [ (col, pa_aln_resnums[pacol], pa_aln[chain_id][pacol]) for (col, pacol) in col_pacol if pa_aln_resnums[pacol] != '-' ]

	return col_resnum_aa

if __name__ == "__main__":
	options = parseCommandLine(sys.argv[1:])
	model = openModel(options['pdb_file'])
	chain = model[options['chain_id']]
	nonhet_chain = getNonHetResidues(chain)
	if 'refid' in options:
		col_resnum_aa = alignChainToRefId(options['refid'], options['aln.fa'],
										options['chain_id'], nonhet_chain)
	else:
		col_resnum_aa = alignChainToAln(options['aln.fa'], options['chain_id'], nonhet_chain)
	
	for c_r_a in col_resnum_aa:
		print '\t'.join(map(str, c_r_a))

