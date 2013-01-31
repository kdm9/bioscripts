# this file should be source()-able to import this function

km.peak.pick <- function (data){
	#get runmean, runsd
	#then, as per old script:
	# wt_mean <- (s1 + s2)/2
	# wt_kmean <- runmean(wt_mean,5)
	# wt_ksd = 5 * runsd(wt_mean,5) # 3-sigma should be good enough
	# wt_upper <- wt_kmean + wt_ksd
	# wt_lower <- wt_kmean - wt_ksd
	# plot(wt_samples[,1:2], pch="+", main="Wt")
	# lines(0:99,wt_mean)
	# lines(0:99,wt_kmean, col="red")
	# lines(0:99,wt_upper, col="red", lty=2)
	# lines(0:99,wt_lower, col="red", lty=3)
	# points(wt_samples[wt_samples[,2] > wt_upper & wt_samples[,3]==3,1:2])
	# removed <- as.vector(as.numeric(row.names(wt_samples[wt_samples[,2] > wt_upper,1:2])))
	# ovral[removed,2] = NA
	# wt_samples <- ovral[ovral[,3]==3 | ovral[,3]==4,]
	# plot(wt_samples[,1:2], pch="+", type="o", main="Wt")
	# lines(lowess(wt_samples[,1:2], na.rm=True))
	# s1 <- ovral[ovral[,3]==3,2]
	# s2 <- ovral[ovral[,3]==4,2]
	# wt_mean <- data.frame(s1=s1, s2=s2)
	# wt_mean[,3] <- rowMeans(wt_mean, na.rm=TRUE)
	# plot(wt_mean[,3])
	# 
	# points(wt_samples[wt_samples[,2] > wt_upper & wt_samples[,3]==4,1:2])
	# ovral[ovral[ovral[,2] > wt_upper & ovral[,3]==3,1] & ovral[,3]==3,]
	# #wt_upper[wt_samples[wt_samples[,2] > wt_upper & wt_samples[,3]==3,1]]
	# 
	# ein5_samples = ovral[ovral[,3]==1 | ovral[,3]==2,1:2]
	# plot(ein5_samples, pch="+", main="ein5")

}
