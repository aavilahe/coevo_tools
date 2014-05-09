# struct_viz #

These are scripts to visualize scores, p-values,
and labels onto structures (PDB files).

## Example usage ##

```bash
# extract chain `B' sequence from ProtX.pdb
python extract_seq.py ProtX.pdb B > ProtX_B.map 
# map resnums to alignment column
python map_column_to_resnum.py --alignment=orthosX.phy --chainMap=ProtX_B.map > ProtX_resnum_col.map 
# map co-evolution scores to residues
python make_attributes.py --LeftMap=ProtX_resnum_col.map Results.tab > ProtX_attributes.txt
```

### `extract_seq.py` ###

Extracts residues for a chain from ATOM records.

```bash
usage: extract_seq.py in.pdb chain
output: in_chain.fa, in_chain.tab
```

### `map_column_to_resnum.py` ###

Takes phylip alignment as input and generates
3 mappings

1. Column to reference sequence
2. Reference sequence position to PDB chain sequence position
3. PDB chain sequence position to PDB chain resnum

And prints a map of Column to PDB chain resnum

### `make_attributes.py` ###

Loads map of Column to PDB chain resnum and tabular co-evolution results file.
Writes chimera readable attributes file, one attribute per column (skips Alignment_Column columns).




