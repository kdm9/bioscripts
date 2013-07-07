
ma = read.table("multiallelic.txt", sep="\t")
ids = data.frame(do.call(rbind, strsplit(as.character(ma$V1), ".",fixed=T)))
multialleic_pos = as.numeric(as.character(ids[,3]))
hist(multialleic_pos, breaks=100)
print("last marker at this many bases: (should be ~~ chr size)")
max(multialleic_pos)
