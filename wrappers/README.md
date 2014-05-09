# Wrappers for various coevolution methods #

## 1. mfDCA
Call matlab to run mfDCA with default options
- `runDCA.sh in.fa out.mfDCA`
- `runDCA_DIR.sh /path/to/DIR /path/to/OUTDIR`
- source: <http://dca.ucsd.edu/DCA/DCA.html>
- *NOTE:* add `mfDCA_support/` to matlab path

## 2. plmDCA
Call matlab to run plmDCA with default options, limit 1 processor
- `runPlmDCA.sh in.fa out.plmDCA`
- source: <http://plmdca.csc.kth.se/>
- *NOTE:* add `plmDCA_support/` to matlab path

## 3. hpDCA
Call matlab to run hpDCA with default options, and 32 patterns
- `runHpDCA.sh in.fa out.hpDCA 32`
- source: <http://www.ploscompbiol.org/article/fetchSingleRepresentation.action?uri=info:doi/10.1371/journal.pcbi.1003176.s002>
- *NOTE:* add `hpDCA_support/` to matlab path

## 4. PSICOV
Run PSICOV with default options, min sequence separation set to 1
- `runPSICOV.sh in.psi out.PSICOV`
- source: <http://bioinfadmin.cs.ucl.ac.uk/downloads/PSICOV/>

