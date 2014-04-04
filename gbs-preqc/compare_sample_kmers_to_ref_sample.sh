#!/bin/bash
set -x

function usage() {
	echo "compare_sample_kmers_to_ref_sample.sh"
	echo "	Compares the Kmer distribution of a sample to that of a reference sample"
	echo
	echo "USAGE:"
	echo "	compare_sample_kmers_to_ref_sample.sh <plate_name> <reference_jelly_hash> <K> <num_reads>"
}


if [ $# -ne 4 ]
then
	usage
	exit - 1
fi

plate=$1
#sample=E5 looped through below
jellyREF=$2
KMERSIZE=$3
N_reads=$4

JELLYFISH=jellyfish
KAT=~norman/applications/KAT/src/kat

#loop through sample files within a plate (Plate hardcoded above)
cat - | parallel --jobs -1 \
       	KatOUTFILE=kat_${plate}_{}_vs_${jellyREF}_kmer_${KMERSIZE} \; \
       	JellyOUTFILE=jelly_${plate}_{}_${KMERSIZE} \; \
	$KAT comp -o \$KatOUTFILE $jellyREF \$\{JellyOUTFILE\}_0
#	sample_FWD=~/Analysis/Brachypodium/exports/${plate}_export_good_clip/sample_{}-1-clipped_filtered.sorted.fq \; \
#	sample_REV=~/Analysis/Brachypodium/exports/${plate}_export_good_clip/sample_{}-2-clipped_filtered.sorted.fq \; \
#	sample_SINGLES=~/Analysis/Brachypodium/exports/${plate}_export_good_clip/sample_{}-singles-clipped_filtered.fq \; \
#	if \[ \! -f \$JellyOUTFILE \] \; then $JELLYFISH count -m$KMERSIZE -C -s 1000000000 -o \$JellyOUTFILE \<\(cat  \$sample_FWD \$sample_REV \$sample_SINGLES \| seqtk sample - $N_reads\) \; fi\; \
