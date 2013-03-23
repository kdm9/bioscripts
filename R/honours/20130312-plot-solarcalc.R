args <- commandArgs(trailingOnly = TRUE)
print(args)
sc <- read.csv(args[1])
names(sc)
sc$dt <- paste(sc$Date, sc$Time)
sc$DateTime <- as.POSIXlt(sc$dt, format="%m/%d/%Y %I:%M %p")

day <- sc[1:1440,]

pdf(args[2])
plot(day$DateTime, day$Total.Solar..Watt.m2., type='l',main="September 1 2012", xlab="Time", ylab="Total Irradiance")
dev.off()
