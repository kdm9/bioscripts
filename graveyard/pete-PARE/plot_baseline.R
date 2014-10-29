library(doMC)
registerDoMC(cores=12)
library(foreach)
library(iterators)

args <- commandArgs(trailingOnly=T)

deg <- read.csv(args[1])
targets <- read.csv(args[2])

agis <- isplit(deg, deg$rname)

overall.hist <- data.frame(rname=character(), pos=numeric(), count=numeric(), m_mapq=numeric())

foreach(agi=agis)%dopar%{
	seq.len = targets[targets[,1] == agi$key[[1]], 2]
	agi$value$pos <- agi$value$pos / seq.len
	overall.hist <- merge(overall.hist, data.frame(agi$value)[,2:5],all=T)
	#by=intersect(names(overall.hist), names(data.frame(agi$value)[,2:5])))
}
pdf(paste(args[3],".pdf", sep=""))
plot(overall.hist$pos, overall.hist$count)
dev.off()
write.csv(paste(args[3],".csv", sep=""))
