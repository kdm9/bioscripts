
# we dont actually need to modify the temp of the "low light" coastal condition
#wol = read.csv("WollongongCurrent30Light.csv")

wol <- read.csv("WollongongCurrent100Light.csv")
inland <- wol

## amplify temp variation by
temp.multi <- 1.9

# Get vector of day mean temps (one per minute record)
num.days <- nrow(inland) / 1440
day.index <- rep(1:num.days, each = 1440)
day.means <- rep(tapply(inland$ChamTemp,day.index,function (x) mean(x) ),each = 1440)

inland$ChamTemp <- day.means + ((inland$ChamTemp - day.means) * temp.multi)

write.csv(inland,file="WolInland.csv",row.names=FALSE,quote=FALSE)

png("WolInland.png")
plot(wol$ChamTemp[1:(10*1440)],type="l",ylim=c(0,30))
lines(inland$ChamTemp[1:(10*1440)],type="l",col="red",ylim=c(0,30))
legend("bottomright", lty=1, legend=c("Coastal", "Inland"), col=c("black", "red"))
dev.off()
