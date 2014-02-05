#!/bin/bash

plate=$1
sample=$2
KMERSIZE=$3

JELLYFISH=jellyfish
REF_FWD=~/Analysis/Brachypodium/exports/${plate}_export_good_clip/sample_${sample}-1-clipped_filtered.sorted.fq
REF_REV=~/Analysis/Brachypodium/exports/${plate}_export_good_clip/sample_${sample}-2-clipped_filtered.sorted.fq
REF_SINGLES=~/Analysis/Brachypodium/exports/${plate}_export_good_clip/sample_${sample}-singles-clipped_filtered.fq


$JELLYFISH count -m$KMERSIZE -C -s 1000000000 -o ref_${plate}_${sample}_${KMERSIZE}.jelly <(cat $REF_FWD $REF_REV $REF_SINGLES) 
