# Usage - structure visualization #
These are scripts to visualize scores, p-values,
and labels onto structures (PDB files).

## `convert_to_attributes.sh` ##
Wrapper that takes care of mapping columns to residues and formatting 
results as chimera residue attributes.

```bash
usage: ./convert_to_attributes.sh summary_results.tab orthos.fa \
                                  refid chain prot.pdb > prot_chain.attr
example: ./convert_to_attributes.sh BestVifCoevoStats.tab vif.fa \
                                  0_HIV1_h_L b 4N9F.pdb1 > 4N9F_b.attr
```

### `map_column_to_resnum.py` ###
Maps alignment columns to resnums and prints a mapping of
Alignment columns to PDB chain resnums.

**Assumes sequence alignment in fasta format**

**Requires a sequence aligner that outputs a _fasta_ alignment**

```python
# check lines 21, 22, 92 in map_column_to_resnum.py
   21    PROFILE_ALN_AND_OPTIONS = 'fmuscle -profile -in1 %s -in2 %s -out /dev/stdout'
   22    PAIRWISE_ALN_AND_OPTIONS = 'needle -auto -asequence %s -bsequence %s -stdout -aformat3 fasta'
   .
   .
   .
   92        cmd = (CMD_TEMPLATE % (fa1, fa2)).split()
```

```bash
usage: python ./map_column_to_resnum.py -r refid chain prot.pdb orthos.fa > prot.pdb_chain.col2res
```

### `make_attributes.py` ###
Writes chimera readable attributes file from alignment column mapping and
co-evolution analysis results.

`make_attributes.py` assumes results are tab delimited, one residue per line.
- Column 1: residue position
- Columns 2-last: summary scores, p-values, or labels to be converted to attributes.

```bash
usage: make_attributes.py summary_results.tab prot.pdb_chain.col2res > prot_chain.attr
```

