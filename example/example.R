#!/bin/Rscript
# example.R -- shows how to use tabIO.R functions

source('../null_utils/tabIO.R')

# load *.mfDCA_tab
dca_tab_fn = 'mfDCA/vif_A3G.mfDCA_tab'
dca_tab = loadTab_mfDCA(dca_tab_fn)

head(dca_tab)

