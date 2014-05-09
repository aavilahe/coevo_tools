#!/usr/bin/env python
''' extract seq from pdb ATOM records '''

import sys


def seq1(seq, custom_map={'Ter': '*'}, undef_code='X'):
	''' stolen from Biopython:
		https://github.com/biopython/biopython/blob/master/Bio/Data/IUPACData.py
		https://github.com/biopython/biopython/blob/master/Bio/SeqUtils/__init__.py
	
	'''

	protein_letters = "ACDEFGHIKLMNPQRSTVWY"
	extended_protein_letters = "ACDEFGHIKLMNPQRSTVWYBXZJUO"
	protein_letters_1to3  = {
		'A': 'Ala', 'C': 'Cys', 'D': 'Asp',
		'E': 'Glu', 'F': 'Phe', 'G': 'Gly', 'H': 'His',
		'I': 'Ile', 'K': 'Lys', 'L': 'Leu', 'M': 'Met',
		'N': 'Asn', 'P': 'Pro', 'Q': 'Gln', 'R': 'Arg',
		'S': 'Ser', 'T': 'Thr', 'V': 'Val', 'W': 'Trp',
		'Y': 'Tyr',
	}
	protein_letters_1to3_extended = dict(list(protein_letters_1to3.items()) + list({
		'B': 'Asx', 'X': 'Xaa', 'Z': 'Glx', 'J': 'Xle',
		'U': 'Sel', 'O': 'Pyl',
	}.items()))

	protein_letters_3to1 = dict((x[1], x[0]) for x in
							protein_letters_1to3.items())
	protein_letters_3to1_extended = dict((x[1], x[0]) for x in
									protein_letters_1to3_extended.items())

	onecode = dict((k.upper(), v) for k, v in 
			protein_letters_3to1_extended.items())
	onecode.update((k.upper(), v) for (k, v) in custom_map.items())
	seqlist = [seq[3*i:3*(i+1)] for i in range(len(seq) // 3)]
	return ''.join(onecode.get(aa.upper(), undef_code) for aa in seqlist)

def get_residues(ATOM_records, chain):
	''' extract residue and residue number in chain from ATOM records '''

	residues = dict()
	for line in ATOM_records:
		resnum = int(line[22:26])
		if line[21] == chain and resnum not in residues:
			resname = line[17:20]
			
			# Biopython >= 1.63 #
			# resAA = Bio.SeqUtils.seq1(resname)
			resAA = seq1(resname)
			residues[resnum] = resAA
	return residues

def sort_residues(residues):
	sorted_residues = [ (resnum, residues[resnum]) for resnum in sorted(residues.iterkeys()) ]
	return sorted_residues

if __name__ == "__main__":
	usg = 'usage: %s in.pdb chain' % sys.argv[0]
	if len(sys.argv) != 3:
		print >>sys.stderr, usg
		sys.exit(1)
	
	pdbfn = sys.argv[1]
	chain = sys.argv[2]

	ATOM_records = [ line.rstrip('\n\r') for line in open(pdbfn, 'r') if line[:6] == 'ATOM  ' ]

	sorted_residues = sort_residues(get_residues(ATOM_records, chain))

#	# print fa
#	fa_fn = '%s.%s.fa' % (pdbfn, chain)
#	fa_fh = open(fa_fn, 'w')
#	print >>fa_fh, '>%s' % fa_fn
#	print >>fa_fh, ''.join([ resAA for (resnum, resAA) in sorted_residues ])
#	fa_fh.close()
#
	# print tab
	#tab_fn = '%s.%s.tab' % (pdbfn, chain)
	#tab_fh = open(tab_fn, 'w')
	for (resnum, resAA) in sorted_residues:
		print '%s\t%s' % (resnum, resAA)
	#tab_fh.close()

