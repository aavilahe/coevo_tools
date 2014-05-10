# Usage - Wrappers #
## Coevolution ##
These scripts facilitate calling methods from the command line with
default or specified parameters.

### mfDCA
Call matlab to run mfDCA with default options.
- source: <http://dca.ucsd.edu/DCA/DCA.html>

```bash
usage: ./runDCA.sh in.fa out.mfDCA
```

### plmDCA (symmetric) 
Call matlab to run plmDCA with default options, and set number of cpus.
- source: <http://plmdca.csc.kth.se/>
- _NOTE: Specifying a single cpu does not require MATLAB PARALLEL COMPUTING TOOLBOX_

```bash
usage, 8 cpus: ./prunPlmDCA.sh in.fa out.plmDCA 8
```

### hpDCA
Call matlab to run hpDCA with default options, and set number of patterns.
- source: [Code S1 of doi:10.1371/journal.pcbi.1003176](http://www.ploscompbiol.org/article/fetchSingleRepresentation.action?uri=info:doi/10.1371/journal.pcbi.1003176.s002)
- _NOTE: add `hpDCA_support/` to matlab path_

```bash
usage, 32 patterns: ./runHpDCA.sh in.fa out.hpDCA 32
```

### PSICOV
Run PSICOV with default options with min sequence separation set to `1`.
and initial rho to `0.001`.
- source: <http://bioinfadmin.cs.ucl.ac.uk/downloads/PSICOV/>

```bash
usage: ./runPSICOV.sh in.psi out.PSICOV
```

## Phylogenetic inference ##

### FastTree
Light wrapper to run FastTree with `-gamma -nosupport -wag`.
Final model parameters (eg. alpha) and progress are output to stderr.
- source: <http://www.microbesonline.org/fasttree/>

```bash
usage: ./fasttree.sh in.phy out.tre
usage: ./fasttree.sh in.phy out.tre 2> log.txt
```

### RAxML (PTHREADS)
Light wrapper to run RAxML with `-f a -m PROTGAMMAWAGF`.
Edit `NBOOT`, `RXOUT`, and `-T 14` to set the number of bootstraps,
RAxML's working directory, and number of threads used.
- source: <http://www.exelixis-lab.org/web/software/raxml>

```bash
usage: ./rax.sh in.phy
```

