# Usage - structure visualization #
These are scripts to visualize scores, p-values,
and labels onto structures (PDB files).

## `convert_to_attributes.sh` ##
Wrapper that takes care of mapping columns to residues and formatting 
results as chimera residue attributes.

```bash
usage: ./convert_to_attributes.sh results.tab orthos.phy \
                                  refid chain prot.pdb > prot_chain.attr
example: ./convert_to_attributes.sh BestVifCoevoStats.tab vif.phy \
                                  0_HIV1_h b 4N9F.pdb1 > 4N9F_b.attr
```

### `extract_seq.py` ##
Extracts residues and resnum for specified chain from ATOM records.
Output is tab delimited.
- Column 1: resnum
- Column 2: residue

```bash
usage: ./extract_seq.py protX.pdb B > protX_chainB.residues
```

### `map_column_to_resnum.py` ###
Maps alignment columns to resnums and prints a mapping of
Alignment columns to PDB chain resnums.

Takes phylip alignment as input and generates 3 intermediate mappings:

1. Alignment column to reference sequence position
2. Reference sequence position to PDB chain sequence position
3. PDB chain sequence position to PDB chain resnum

**Requires a sequence aligner that outputs a _fasta_ alignment**

```python
# check lines 11, 121 in map_column_to_resnum.py
ALIGNER_AND_OPTIONS = 'msaprobs -num_threads 12 %s' # %s is the input filename
.
.
.
aln_results = Popen( (ALIGNER_AND_OPTIONS % tmpfn).split(), stdout=PIPE ).communicate()[0] # keep stdout
```

```bash
usage: ./map_column_to_resnum.py Xref Xorthos.phy protX_chainB.residues > protX_chainB.col2res
```

### `make_attributes.py` ###
Writes chimera readable attributes file from alignment column mapping and
co-evolution analysis results.

`make_attributes.py` assumes results are tab delimited, one residue per line.
- Column 1: residue position
- Columns 2-last: summary scores, p-values, or labels to be converted to attributes.

```bash
usage: make_attributes.py XSummaryResults.tab protX_chainB.col2res > protX_chainB.attr
```

