library(reshape2)
library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)
print(args)
c1 <- read.csv(args[1])
c1$DateTime <- as.POSIXct(paste(c1$Date, c1$Time), format="%m/%d/%Y %I:%M %p")
day1 <- c1[1:1440,]

c2 <- read.csv(args[2])
c2$DateTime <- as.POSIXct(paste(c2$Date, c2$Time), format="%m/%d/%Y %I:%M %p")
day2 <- c2[1:1440,]

c3 <- read.csv(args[3])
c3$DateTime <- as.POSIXct(paste(c3$Date, c3$Time), format="%m/%d/%Y %I:%M %p")
day3 <- c3[1:1440,]


plt.dat <- data.frame(time=day1$DateTime, day1=day1$LED1, day2=day2$LED1, day3=day3$LED1)
plt.dat <- melt(plt.dat, id=c("time"))

write.csv(plt.dat, file="plt_dat.csv")

ggplot(data=a, aes(x=time, y=value, colour=variable)) +
  geom_line(size=1) +
  scale_x_datetime() +
  theme_bw()
