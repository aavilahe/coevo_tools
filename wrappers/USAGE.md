### `fasttree.sh`
Light wrapper to run FastTree with `-gamma -nosupport -wag`
Final model parameters (eg. alpha) and progress output to stderr.

```bash
usage: ./fasttree.sh in.phy out.tre
usage: ./fasttree.sh in.phy out.tre 2> log.txt
```

### `rax.sh`
Light wrapper to run RAxML with `-f a -m PROTGAMMAWAGF`
Edit `NBOOT`, `RXOUT`, and `-T 14` to set the number of bootstraps,
RAxML's working directory, and number of threads used.

```bash
usage: ./rax.sh in.phy
```

