#!/usr/bin/env python
''' make-psicov-qsub-array-jobs.py -- find psicov formatted simsulated alignments, makes array jobs for each dir

	This example assumes:
		- concatenated left and right protein alignments in the same file
		- psicov formatted (one sequence per line, no seq ids)
		- you want to run `runPSICOV'

'''

import sys
import glob
from os import listdir, makedirs
from os.path import basename, exists


TOP_LVL_DIR = "/path/to/data/for/example/TCS_benchmark"

# Let's say we have 100s of simulation directories burried deep, with the following naming scheme:
# /path/to/data/for/example/TCS_benchmark/subsamples/psifa/master-5000/HisKA_RR-5000-0-sims
# Use glob to collect a list of directory names that each contain 1000s of simulated alignments
SIM_DIRS = glob.glob(TOP_LVL_DIR+'/subsamples/psifa/master-*/*-sims')

# directory to put the results, be careful with overwriting files with the same filenames
OUT_PATH = TOP_LVL_DIR + '/output/PSICOV'

def make_script(simdir, simlist, outdir):
	''' sets up qsub script with simdir, sim basename list, and output dir

	'''

	num_sims = len(simlist)

#### #### EDIT THIS TO SPECIFY YOUR SGE RESOURCES AND RUNTIME OPTIONS #### ####

	script = '''\
#!/bin/bash
# calls runPSICOV-SSE2 on all %d alignments in '%s'
#
#$ -S /bin/bash
#$ -o /this/is/where/to/put/stdout
#$ -e /this/is/where/to/put/stderr
#$ -l mem_free=1.5G
#$ -l arch=linux-x64
#$ -l netapp=100M,scratch=100M
#$ -l h_rt=10:00:00
#$ -r yes
#$ -V
#$ -t 1-%d

# basename input
PSI_ARRAY=(
%s
)

TASK_IDX=$((${SGE_TASK_ID} - 1))
PSI_CURR=${PSI_ARRAY[${TASK_IDX}]}
PSI_OUT=${PSI_CURR%%.psi}.PSICOV
HN="$(hostname)"

echo "starting runPSICOV: ${TASK_IDX} at $(date +%%Y-%%m-%%d.%%H:%%M:%%s) on ${HN}"

PSI_IN_FULL_PATH="%s/${PSI_CURR}"
PSI_OUT_FULL_PATH="%s/${PSI_OUT}"

#echo "${PSI_IN_FULL_PATH}" "${PSI_OUT_FULL_PATH}"
runPSICOV "${PSI_IN_FULL_PATH}" "${PSI_OUT_FULL_PATH}"

echo "finished at $(date +%%Y-%%m-%%d.%%H:%%M:%%s)"
''' % (num_sims, simdir, num_sims, '\n'.join(simlist), simdir, outdir)

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####

	return script	

if __name__ == "__main__":
	if len(sys.argv) != 1:
		sys.exit("usage: %s" % sys.argv[0])
	
	for jb, simdir in enumerate(SIM_DIRS):
		outdir = OUT_PATH + simdir.split('psifa')[1]
		if not exists(outdir):
			makedirs(outdir)
		simlist = [ basename(sim) for sim in glob.glob(simdir+'/sim?*.psi') ]
		script = make_script(simdir, simlist, outdir)
		QSUB = open('jobs/psi-%d__%s.qsub' % (jb, basename(simdir)), 'w')
		print >>QSUB, script



