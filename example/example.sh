#!/bin/bash
# example.sh -- shows off how to use some of the utilities

# fasta to phy
../fmt_utils/fasta_to_phy.py < vif.fa > vif.phy
../fmt_utils/fasta_to_phy.py < A3G.fa > A3G.phy

# merge fastas
../fmt_utils/concatenate_fastas.py vif.fa A3G.fa > vif_A3G.fa

# split fasta
#../fmt_utils/split_faa_on_col.py vif_A3G.fa 324 vif.fa A3G.fa

# use runDCA.sh
mkdir -p mfDCA/
../wrappers/runDCA.sh vif_A3G.fa mfDCA/vif_A3G.mfDCA

#  format mfDCA output
../fmt_utils/make_tab.py mfDCA 324 < mfDCA/vif_A3G.mfDCA > mfDCA/vif_A3G.mfDCA_tab

# tabIO.R
Rscript example.R



