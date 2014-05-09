#!/bin/bash
# runHpDCA.sh -- tell matlab to run inverse_hopfield_potts1() and
#                  inverse_hopfield_potts2() with default options

if [ $# -ne 3 ]; then
	echo "$0 in.fa out.hpDCA numPatterns"
	exit 1
fi

IN="'${1}'"
OUT="'${2}'"
NPAT="${3}"

CALL="hpDCAwrap(${IN},${OUT},${NPAT}) ; quit"

echo "Call: ${CALL}"

matlab -nojvm -nodesktop -nodisplay -nosplash -r "${CALL}" < /dev/null

