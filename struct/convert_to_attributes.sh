#!/bin/bash
# Generates chimera attributes from co-evolution results

__SRC_PATH="$(dirname $0)" # change if you move or link


USG="usage: $0 results.tab orthos.phy refid chain prot.pdb > prot_chain.attr"

if [ $# -ne 5 ]; then
	echo ${USG}
	exit 1
fi

TAB=${1}
ALN=${2}
REF=${3}
CHN=${4}
PDB=${5}

# extract chain (eg. chain 'B') from pdb file
RN_AA="$(basename ${PDB})_${CHN}.residues"
python ${__SRC_PATH}/extract_seq.py ${PDB} ${CHN} > ${RN_AA}

# map alignment columns to pdb residues
AC_RN="${RN_AA%.residues}.col2res"
python ${__SRC_PATH}/map_column_to_resnum.py ${REF} ${ALN} ${RN_AA} > ${AC_RN}

# load results, col2resnum map, print in attributes format
python ${__SRC_PATH}/make_attributes.py ${TAB} ${AC_RN}

