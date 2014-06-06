# Usage
These should help submitting thousands of jobs to an SGE cluster
*Test with small jobs first! Don't make your sysadmin angry.*

## skeleton code for creating many array jobs

### `make-infcalc-qsub-array-jobs.py`
Edit to your liking, shows how to use runInfCalc wrapper with
left and right alignments in phylip format.

### `make-psicov-qsub-array-jobs.py`
Edit to your liking, shows how to use runPSICOV wrapper with
concatenated alignments in "psicov format"

## sge utilities

### qchain
After making tens or hundreds of qsub scripts with `make-infcalc-qsub-array-jobs.py`
or `make-psicov-qsub-array-jobs.py`, submit them in a chained fashion with
`qchain`. The next job array will not start until all tasks in the first job array
have completed.

### qkill_all_jobs
`qdel` all jobs you own.

