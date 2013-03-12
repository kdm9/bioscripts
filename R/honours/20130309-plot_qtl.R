library(reshape2)
library(ggplot2)

# First, a QTL
aa <- rnorm(10)
ab <- rnorm(10) + 5
bb <- rnorm(10) + 15

g <- data.frame(aa=aa,ab=ab,bb=bb)
g <- melt(g)
pdf("qtl.pdf", width=3, height=2)
ggplot(g, aes(x=variable, y=value)) +
  geom_point() +
#  ggtitle("QTL") +
  scale_x_discrete(name="Genotype") +
  scale_y_continuous(name="Quantitative Trait") +
  theme_bw()
dev.off()

# Now, not a QTL
aa <- rnorm(10)
ab <- rnorm(10)
bb <- rnorm(10)

g <- data.frame(aa=aa,ab=ab,bb=bb)
g <- melt(g)
pdf("not_qtl.pdf", width=3, height=2)
ggplot(g, aes(x=variable, y=value)) +
  geom_point() +
#  ggtitle("Not a QTL") +
  scale_x_discrete(name="Genotype") +
  scale_y_continuous(name="Quantitative Trait") +
  theme_bw()
dev.off()
