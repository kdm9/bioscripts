library(ggplot2)
library(reshape)
library(grid)

#source("http://egret.psychol.cam.ac.uk/statistics/R/extensions/rnc_ggplot2_border_themes.r")

spectra <- read.csv("20130308-AllSpectra.csv")
names(spectra)

plt.spectra <- spectra[,c(1,6,8:9)]
names(plt.spectra) <- names(spectra[,c(1:2,4:5)])
names(plt.spectra)[4] = "LED"
names(plt.spectra)
spec <- melt(plt.spectra, id="WL")
spec
cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

pdf("all_spectra.pdf", width=6, height=4)
base_size = 12
ggplot(data=spec, aes(x=WL, y=value, colour=variable)) +
#  ggtitle("Relative Spectral Power\nDensity of Light Sources") +
  geom_line(size=2) +
  scale_x_continuous(name="\nWavelength (nm)") +
  scale_y_continuous(name="Normalised Spectral Power Density\n") +
  scale_colour_manual(values=cbPalette) +
  theme_bw() +
  theme(
    legend.position = c(0.80, 0.76),
    legend.title=element_blank(),
    panel.margin = unit(c(1.5,1.5,1.5,1.5),"cm")
    )

dev.off()
