bcfix = read.csv("/home/kevin/uw/hons/notebook/2013-05/20130515-BotrivierCurrent.csv")
bcd1fix  <- bcfix[271:(1440+270),]
tcfix = read.csv("/home/kevin/uw/hons/notebook/2013-05/20130515-TilbaCurrent.csv")
tcd1fix  <- tcfix[271:(1440+270),]
tffix = read.csv("/home/kevin/uw/hons/notebook/2013-05/20130515-TilbaFuture.csv")
tfd1fix  <- tffix[271:(1440+270),]
bffix = read.csv("/home/kevin/uw/hons/notebook/2013-05/20130515-BotrivierFuture.csv")
bfd1fix  <- bffix[271:(1440+270),]
mfix = read.csv("/home/kevin/solarcalc/CarolineSolarCalc/MiddlebergCurrent.csv")
md1fix  <- mfix[1:1440,]


pdf("CarolineSolarcalc.pdf")
####Botrivier Temp and light
plot(
	bcd1fix$ChamTemp,
	main="Botrivier (black), tilba (green), middleberg (red)",
	type="l",
	ylim=c(0,30),
	xlab="Mintutes (from midnight)",
	ylab="Deg C"
)
lines(
	tcd1fix$ChamTemp,
	type="l",
	ylim=c(0,30),
	col="green"
)
lines(
	md1fix$ChamTemp,
	type="l",
	ylim=c(0,30),
	col="red"
)
plot(
	rowSums(bcd1fix[,5:11]),
	main="Botrivier (black), tilba (green), middleberg (red)",
	type="l",
	ylim=c(0,2000),
	xlab="Mintutes (from midnight)",
	ylab="Total Solar Output (Watt per m2)"
)
lines(
	rowSums(tcd1fix[,5:11]),
	type="l",
	ylim=c(0,2000),
	col="green"
)

lines(
	rowSums(md1fix[,5:11]),
	type="l",
	ylim=c(0,2000),
	col="red"
)

#### TILBA temp + light
plot(
	tcd1fix$ChamTemp,
	main="Tilba (current = black, future = green)",
	type="l",
	ylim=c(0,30),
	xlab="Mintutes (from midnight)",
	ylab="Deg C"
)
lines(
	tfd1fix$ChamTemp,
	type="l",
	ylim=c(0,30),
	col="green"
)
plot(
	tcd1fix$Total.Solar..Watt.m2.,
	main="Tilba (current = black, future = green)",
	type="l",
	ylim=c(0,1100),
	xlab="Mintutes (from midnight)",
	ylab="Total Solar Output (Watt per m2)"
)
lines(
	tfd1fix$Total.Solar..Watt.m2.,
	type="l",
	ylim=c(0,1100),
	col="green"
)

plot(
	bcd1fix$ChamTemp - tcd1fix$ChamTemp,
	main="Temp Difference between Tilba and Botrivier",
	type="l",
	ylim=c(0,5),
	xlab="Mintutes (from midnight)",
	ylab="Delta C"
)

dev.off()

