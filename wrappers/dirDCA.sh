#!/bin/bash
# call runDCA.sh on each *.fa in a directory. Output to named subdirectory

if [ $# -ne 2 ]; then
	echo "$0 fasta_dir/ out_dir/"
	exit 1
fi

FADIR="${1}"
OUTDIR="${2}"

ARGS=""
for pathname in `find ${1} -iname '*.fa'`; do
	ARGS="${ARGS} ${pathname} ${OUTDIR}/$(basename ${pathname%.fa}.mfDCA)"
done

parallel -j 13 -l 13 -n 2 runDCA -- ${ARGS}
