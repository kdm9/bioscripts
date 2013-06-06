wol = read.csv("WollongongCurrent100Light-firstday.csv")
wol35 = read.csv("WollongongCurrent35Light-firstday.csv")
grif = read.csv("GrifithCurrent100Light-firstday.csv")
mild = read.csv("ZaragozaCurrent100Light-firstday.csv")


png("KengTemps.png")
plot(
	wol$ChamTemp,
	main="Chamber Temp",
	type="l",
	ylim=c(0,32),
	xlab="Time",
	ylab="Deg C"
)
lines(
	wol35$ChamTemp,
	type="l",
	ylim=c(0,32),
	col="green"
)
lines(
	grif$ChamTemp,
	type="l",
	ylim=c(0,32),
	col="red"
)
lines(
	mild$ChamTemp,
	type="l",
	ylim=c(0,32),
	col="blue"
)
legend(
       "bottomright",
       lty=1,
       legend=c("Wollongong 100%", "Wollongong 35%", "Griffith 100%", "Mildura 100%"),
       col=c("black", "green", "red", "blue")
)
dev.off()

png("KengRHs.png")
plot(
	wol$ChamRH,
	main="Chamber RH",
	type="l",
	ylim=c(0,100),
	xlab="Time",
	ylab="Deg C"
)
lines(
	wol35$ChamRH,
	type="l",
	ylim=c(0,100),
	col="green"
)
lines(
	grif$ChamRH,
	type="l",
	ylim=c(0,100),
	col="red"
)
lines(
	mild$ChamRH,
	type="l",
	ylim=c(0,100),
	col="blue"
)
legend(
       "bottomright",
       lty=1,
       legend=c("Wollongong 100%", "Wollongong 35%", "Griffith 100%", "Mildura 100%"),
       col=c("black", "green", "red", "blue")
)
dev.off()

png("KengLight.png")
plot(
	rowSums(wol[,5:11]),
	main="LED Intensity",
	type="l",
	ylim=c(0,2000),
	xlab="Time",
	ylab="Sum of LED intensity"
)
lines(
	rowSums(wol35[,5:11]),
	type="l",
	ylim=c(0,2000),
	col="green"
)
lines(
	rowSums(grif[,5:11]),
	type="l",
	ylim=c(0,2000),
	col="red"
)
lines(
	rowSums(mild[,5:11]),
	type="l",
	ylim=c(0,2000),
	col="blue"
)
legend(
       "topleft",
       lty=1,
       legend=c("Wollongong 100%", "Wollongong 35%", "Griffith 100%", "Mildura 100%"),
       col=c("black", "green", "red", "blue")
)
dev.off()

ratio <- rowSums(wol[,5:11])/rowSums(wol35[,5:11])
png("KengHL.LL_ratio.png")
plot(ratio,type="l",ylim=c(0,4))
dev.off()
