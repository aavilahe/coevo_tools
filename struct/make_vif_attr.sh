#!/bin/bash
# Generates vif attributes file for chimera

SRC="/home/aram/dev-src/struct_viz"

# load, merge, flatten results (removes A3G info, too)
Rscript quickPred.R > FlatVifCoevoStats.tab

# extract vif chain (chain `b') from 4N9F.pdb1
python ${SRC}/extract_seq.py 4N9F.pdb1 b > 4N9F_b.map

# map vif alignment columns to pdb residues
python ${SRC}/map_column_to_resnum.py 0_HIV1_h ../master_alignment/vif.phy 4N9F_b.map > 4N9F_col2resnum.map

# load flat results, col2resnum map, print in attributes format
python ${SRC}/make_attributes.py FlatVifCoevoStats.tab 4N9F_col2resnum.map > vif_attr.txt

