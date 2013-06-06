tem100 = read.csv("/home/kevin/uw/hons/lab/solarcalc/keng/TemoraCurrent100Light-firstday.csv")
tem50 = read.csv("/home/kevin/uw/hons/lab/solarcalc/keng/TemoraCurrent50Light-firstday.csv")
umea = read.csv("/home/kevin/uw/hons/lab/solarcalc/keng/UmeaCurrent100Light-firstday.csv")
zaragoza = read.csv("/home/kevin/uw/hons/lab/solarcalc/keng/ZaragozaCurrent100Light-firstday.csv")


png("KengTemps.png")
####Botrivier Temp and light
plot(
	tem100$ChamTemp,
	main="Chamber Temp",
	type="l",
	ylim=c(0,32),
	xlab="Time",
	ylab="Deg C"
)
lines(
	tem50$ChamTemp,
	type="l",
	ylim=c(0,32),
	col="green"
)
lines(
	umea$ChamTemp,
	type="l",
	ylim=c(0,32),
	col="red"
)
lines(
	zaragoza$ChamTemp,
	type="l",
	ylim=c(0,32),
	col="blue"
)
legend(
       "bottomright",
       lty=1,
       legend=c("Tempora 100%", "Temora 50%", "Umea 100%", "Zaragoza 100%"),
       col=c("black", "green", "red", "blue")
)
dev.off()

png("KengLight.png")
plot(
	rowSums(tem100[,5:11]),
	main="LED Intensity",
	type="l",
	ylim=c(0,2000),
	xlab="Time",
	ylab="Sum of LED intensity"
)
lines(
	rowSums(tem50[,5:11]),
	type="l",
	ylim=c(0,2000),
	col="green"
)
lines(
	rowSums(umea[,5:11]),
	type="l",
	ylim=c(0,2000),
	col="red"
)
lines(
	rowSums(zaragoza[,5:11]),
	type="l",
	ylim=c(0,2000),
	col="blue"
)
legend(
       "topleft",
       lty=1,
       legend=c("Tempora 100%", "Temora 50%", "Umea 100%", "Zaragoza 100%"),
       col=c("black", "green", "red", "blue")
)
dev.off()
