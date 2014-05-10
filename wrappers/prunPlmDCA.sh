#!/bin/bash
# runPlmDCA.sh -- tell matlab to run plmDCA_symmetric() with default options

if [ $# -ne 3 ]; then
	echo "$0 in.fa out.plmDCA Ncpus"
	exit 1
fi

IN="'${1}'"
OUT="'${2}'"

#NCPU=8 # max workers allowed (physical cores)
NCPU="${3}"

CALL="plmDCA_symmetric(${IN},${OUT},0.01,0.01,0.1,${NCPU}) ; quit"

echo "Call: ${CALL}"

matlab -nodesktop -nodisplay -nosplash -r "${CALL}" < /dev/null

