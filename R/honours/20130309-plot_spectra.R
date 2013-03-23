library(ggplot2)
library(reshape)
library(grid)

#source("http://egret.psychol.cam.ac.uk/statistics/R/extensions/rnc_ggplot2_border_themes.r")
setwd("uw/hons/grantProposal/proposal/introSeminar/img/")
spectra <- read.csv("/home/kevin/uw/hons/lab/spectra/20130308-AllSpectra.csv")
cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")


plt.spectra <- spectra[,c(1,6)]
names(plt.spectra) <- names(spectra[,c(1:2)])
spec <- melt(plt.spectra, id="WL")

pdf("all_spectra1.pdf", width=6, height=4)
ggplot(data=spec, aes(x=WL, y=value, colour=variable)) +
#  ggtitle("Relative Spectral Power\nDensity of Light Sources") +
  geom_line(size=2) +
  scale_x_continuous(name="\nWavelength (nm)") +
  scale_y_continuous(name="Normalised Spectral Power Density\n", limits=c(0,2.2)) +
  scale_colour_manual(values=cbPalette) +
  theme_bw() +
  theme(
    legend.position = c(0.80, 0.76),
    legend.title=element_blank(),
    panel.margin = unit(c(1.5,1.5,1.5,1.5),"cm")
    )
dev.off()


plt.spectra <- spectra[,c(1,6,8)]
names(plt.spectra) <- names(spectra[,c(1:2,4)])
spec <- melt(plt.spectra, id="WL")


pdf("all_spectra2.pdf", width=6, height=4)
ggplot(data=spec, aes(x=WL, y=value, colour=variable)) +
  #  ggtitle("Relative Spectral Power\nDensity of Light Sources") +
  geom_line(size=2) +
  scale_x_continuous(name="\nWavelength (nm)") +
  scale_y_continuous(name="Normalised Spectral Power Density\n", limits=c(0,2.2)) +
  scale_colour_manual(values=cbPalette) +
  theme_bw() +
  theme(
    legend.position = c(0.80, 0.76),
    legend.title=element_blank(),
    panel.margin = unit(c(1.5,1.5,1.5,1.5),"cm")
  )
dev.off()



plt.spectra <- spectra[,c(1,6,8:9)]
names(plt.spectra) <- names(spectra[,c(1:2,4:5)])
names(plt.spectra)[4] = "LED"
spec <- melt(plt.spectra, id="WL")


pdf("all_spectra3.pdf", width=6, height=4)
ggplot(data=spec, aes(x=WL, y=value, colour=variable)) +
  #  ggtitle("Relative Spectral Power\nDensity of Light Sources") +
  geom_line(size=2) +
  scale_x_continuous(name="\nWavelength (nm)") +
  scale_y_continuous(name="Normalised Spectral Power Density\n", limits=c(0,2.2)) +
  scale_colour_manual(values=cbPalette) +
  theme_bw() +
  theme(
    legend.position = c(0.80, 0.76),
    legend.title=element_blank(),
    panel.margin = unit(c(1.5,1.5,1.5,1.5),"cm")
  )
dev.off()