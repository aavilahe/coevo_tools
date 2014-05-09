#!/bin/bash
# runDCA.sh -- tell matlab to run dca() with default options

if [ $# -ne 2 ]; then
	echo "$0 in.fa out.mfDCA"
	exit 1
fi

IN="'${1}'"
OUT="'${2}'"

CALL="dca(${IN},${OUT}) ; quit"

echo "Call: ${CALL}"

matlab -nojvm -nodesktop -nodisplay -nosplash -r "${CALL}" < /dev/null

