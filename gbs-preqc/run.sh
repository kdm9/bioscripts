#!/bin/bash

set -x
k=23
for ref in "2 C5" "6 D6" "6 D5" "6 D8" "6 D7"
do

	rplate=plate$(echo $ref | cut -d ' ' -f 1)
	rsamp=$(echo $ref | cut -d ' ' -f 2)
	echo $rplate $rsamp

	bash ~/prog/bio/scripts/gbs-preqc/make_ref_sample_hash.sh $rplate $rsamp $k
	for p in 1 2 3 4 6
	do
		cat ~norman/helper-files/fosn.txt | bash ~/prog/bio/scripts/gbs-preqc/compare_sample_kmers_to_ref_sample.sh plate$p ref_${rplate}_${rsamp}_${k}.jelly_0 $k 1000000
	done
done
