#!/bin/bash
# Runs PSICOV compiled with -msse2 with default options PLUS:
# min sequence separation set to 1
# rho estimate at 0.001

if [ $# -ne 2 ]; then
	echo "usage: $0 in.psi out.PSICOV"
	exit
fi

IN=${1}
OUT=${2}

psicov-sse2 -j 1 -r 0.001 ${IN} > ${OUT}



