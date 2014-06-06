# Usage - Formatting utilities #

## `concatenate_fastas.py`
Concatenates pairs of sequences from two alignments.
Headers must exactly match (seq id and comment) and be unique within each fasta.
Unpaired sequences are skipped, whitespace is removed from sequence.

```bash
usage: ./concatenate_fastas.py left.fa right.fa > left_right.fa
```

## `fasta_to_phy.py`
Convert fasta to "strict" phylip:

- header: `' Nseqs Ncol'`
- one sequence per line
	- first 8 chars are truncated seq ids
	- chars 9,10 are spaces
	- 11th char is first alignment column

Fasta header line is split on whitespace, comment is discarded.
Whitespace is removed from sequence.

```bash
usage: ./fasta_to_phy.py < fasta > phy
```

## `fasta_to_psicov.py`
Convert fasta to PSICOV readable format
	- one sequence per line, no headers
Discard all headers, remove whitespace from sequence.

```bash
usage: ./fasta_to_psicov.py < fasta > psicov
```

## `fix_dummy_pvalues.py`
Compares co-evolution scores measured from an observed alignment to scores from 
alignments simulated under a null distribution to estimate a p-value.
Scores are in a tab delimited format output by `make_tab.py`

_NOTE: relevant scores are in different columns, depending on co-evolution program used_ 

```bash
# typical usage:
./fix_dummy_pvalues.py mfDCA 1000 <(cat sim1.tab sim2.tab ... sim1000.tab) < scores.tab > scores_pvalues.tab
```

## `make_tab.py`
Formats the raw output from co-evolution programs into a tab delimited file.

1. **Sets alignment column indices to start at `0`**
2. **Renumber alignment column indices to match individual alignments (instead of the concatenated alignment)**
3. Removes intra-protein scores
4. `mfDCA` reports mutual information with reweighting (MI_w) and direct information (DI)
5. `infCalc` reports marginal entropies for each column and joint entropies for each column-pair  
		as well as 4 mutual information based scores (MI, MI_Hmin, MI_J, VI)
6. Adds dummy p-values (`nan`) in new column for each score 

```bash
usage: ./make_tab.py fmt last_left < output > output_tab
 fmt: mfDCA, plmDCA, hpDCA, psicov, infCalc
 last_left: length of left protein alignment
```

## `split_faa_on_col.py`
Halve an aligned fasta on a specified column. Does not modify sequence order. Appends `'_L|R'` to
sequence ids, comment is included in output untouched.

```bash
# col: 1,2,3,...,N,N+1,...,K
#       <--Left--| |--Right-->

usage: ./split_faa_on_col.py ali.fa N left.fa right.fa
```


