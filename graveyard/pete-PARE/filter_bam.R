library(Rsamtools)
library(plyr)
args <- commandArgs(trailingOnly=T)

### EXPORT BAM

## Import data from bam
#rname:	reference name
#pos:	ref. mapping position
#mapq:	mapping quality score
#cigar:	CIGAR indel string
bam <- scanBam(args[1], param=ScanBamParam(what=c("rname","pos", "mapq", "cigar")))
bam <- data.frame(bam)

## Filter data
#Remove NA rows (unmapped reads)
bam <- bam[!is.na(bam[,1]),]
bam <- bam[!is.na(bam[,2]),]
#Remove rows with mapq < 20
bam <- bam[bam[,3]>=20,]

## Summarise data to count table
bam.counts <- ddply(bam, .(rname, pos), summarise, count=length(rname), m_mapq=mean(mapq))

## Write filtered bam to CSV
csv_filename <- paste(args[2], "filtered.csv", sep="_")
write.csv(bam.counts, file=csv_filename)

### EXPORT BAM TARGETS
## import header
header <- scanBamHeader(args[1])
#extract targets detail
targets <- data.frame(header[[1]]$targets)

targets_filename <- paste(args[2], "targets.csv", sep="_")
write.csv(targets, file=targets_filename)

