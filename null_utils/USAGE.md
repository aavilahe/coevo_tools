# Usage - Null model utilities #

## `tabIO.R` ##
Functions for loading tab delimited `.tab`s from coevolution method wrappers as data.frames

### `loadTab_<method>()` ###
Functions for loading coevolution scores using various methods after processing with
`fmt_utils/make_tab.py` and `fmt_utils/fix_dummy_pvalues.py`. Adds *Pnormal* and *Pempirical*
for each score.

### `addPemp()` and `addPnorm()` ###
These functions take a data.frame and column names of scores to compute *Pempirical*
and *Pnormal* and adds them as new columns with `r_` and `z_` prefixes.

### *Pbootstrap* values ###
*Pbooststrap* is assumed to have been calculated separately using `fmt_utils/fix_dummy_pvalues.py` after
running `simulate_tools` to generate alignments according to the null model, and running the
appropriate method (followed by `fmt_utils/make_tab.py`) to generate the null distributions of scores for
each column-pair.

