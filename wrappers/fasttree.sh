#!/bin/bash
# fasttree.sh -- runs FastTree with -gamma -nosupport -wag
#				(similar to raxml -m PROTGAMMAWAG -f d) 

if [ "$#" != 2 ]; then
	echo "usage: $0 in.phy out.tre"
	exit 1
fi

ALN=${1}
TRE=${2}

echo -e "Building a tree for ${ALN} in ${TRE}\n\n"

# estimate topology and branch lengths:
FastTree -gamma -nosupport -wag ${ALN} > ${TRE}

