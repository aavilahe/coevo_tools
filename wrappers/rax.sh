#!/bin/bash
#run raxml as follows
#	infer topology from alignment
#		fast bootstrap search
#		optimize branch length
#	gammawagf

if [ $# -ne 1 ]; then
	echo "usage: $0 aln.phy"  >> /dev/stderr
	exit 1
fi

xSeed=${RANDOM:0:7}
pSeed=${RANDOM:0:7}

ALN=${1}
JB=$(basename ${ALN%.phy}_x${xSeed}_p${pSeed})
RXOUT=$(pwd)/RAxML.${JB}
TRE=$(basename ${ALN%.phy}.tre)
NBOOT=1000

mkdir -p ${RXOUT}

raxmlHPC-PTHREADS-SSE3 -n ${JB} -s ${ALN} -m PROTGAMMAWAGF -f a -N ${NBOOT} -x ${xSeed} -p ${pSeed} -T 14 -w ${RXOUT}
cp ${RXOUT}/RAxML_bestTree.${JB} ${TRE}

