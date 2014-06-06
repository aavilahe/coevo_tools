#!/usr/bin/env python
''' make-infcalc-qsub-array-jobs.py -- finds dirs containing simulated alignments, makes array job for each dir

	This example assumes:
		- left and right protein alignments are in separate files
		- phylip formatted
		- you want to run `runInfCalc'

'''

import sys
import glob
from os import listdir, makedirs
from os.path import basename, exists


TOP_LVL_DIR = "/path/to/data/for/example/TCS_benchmark"

# Let's say we have 100s of simulation directories burried deep, with the following naming scheme:
# /path/to/data/for/example/TCS_benchmark/subsamples/phy/master-5000/RR-5000-0-sims
# Use glob to collect a list of directory names that each contain 1000s of simulated alignments
LEFT_SIM_DIRS = glob.glob(TOP_LVL_DIR+'/subsamples/phy/master-*/HisKA*-sims') 
RIGHT_SIM_DIRS = glob.glob(TOP_LVL_DIR+'/subsamples/phy/master-*/RR*-sims')

# infCalc.py (called from runInfCalc) will want to know which seq ids are paired
PAIRS_FILE = TOP_LVL_DIR + '/master_alignment/HisKA_RR.pairs'

# directory to put the results, be careful with overwriting files with the same filenames
OUT_PATH = TOP_LVL_DIR + '/output/infCalc'

def make_script(left_simdir, right_simdir, simlist, outdir, PAIRS_FILE):
	''' sets up qsub script with simdir, sim basename list, and output dir

	'''

	num_sims = len(simlist)

#### #### EDIT THIS TO SPECIFY YOUR SGE RESOURCES AND RUNTIME OPTIONS #### ####

	script = '''\
#!/bin/bash
# calls runInfCalc on all %d alignments in '%s' and '%s'
#
#$ -S /bin/bash
#$ -o /this/is/where/to/put/stdout
#$ -e /this/is/where/to/put/stderr
#$ -l mem_free=300M
#$ -l arch=linux-x64
#$ -l netapp=10M,scratch=10M
#$ -l h_rt=8:00:00
#$ -r yes
#$ -V
#$ -t 1-%d

# basename input
PHY_ARRAY=(
%s
)

TASK_IDX=$((${SGE_TASK_ID} - 1))
PHY_CURR=${PHY_ARRAY[${TASK_IDX}]}
HN="$(hostname)"

echo "starting runInfCalc: ${TASK_IDX} at $(date +%%Y-%%m-%%d.%%H:%%M:%%s) on ${HN}"

HK_FULL_PATH="%s/${PHY_CURR}"
RR_FULL_PATH="%s/${PHY_CURR}"
PHY_FULL_OUT="%s"
SEQID_PAIRS="%s"

runInfCalc --vir_aln=${HK_FULL_PATH} --host_aln=${RR_FULL_PATH} --outdir=${PHY_FULL_OUT} \\
			--seqID_pairs=${SEQID_PAIRS} --vir_keep=all --host_keep=all --remove_gapped=999.999
#echo ${HK_FULL_PATH} ${RR_FULL_PATH} ${PHY_FULL_OUT} ${SEQID_PAIRS}

echo "finished at $(date +%%Y-%%m-%%d.%%H:%%M:%%s)"
''' % (num_sims, left_simdir, right_simdir,
		num_sims,
		'\n'.join(simlist),
		left_simdir, right_simdir, outdir,
		PAIRS_FILE)

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####

	return script

if __name__ == "__main__":
	if len(sys.argv) != 1:
		sys.exit("usage: %s" % sys.argv[0])
	
	for jb, left_simdir in enumerate(LEFT_SIM_DIRS):
		right_simdir = RIGHT_SIM_DIRS[jb]
		outdir = OUT_PATH + left_simdir.split('phy')[1].replace('HisKA','HisKA_RR')
		if not exists(outdir):
			makedirs(outdir)
		simlist = [ basename(sim) for sim in glob.glob(left_simdir+'/sim?*.phy') ]
		script = make_script(left_simdir, right_simdir, simlist, outdir, PAIRS_FILE)
		QSUB = open('jobs/phy-%d__%s.qsub' % (jb, basename(left_simdir)), 'w')
		print >>QSUB, script

