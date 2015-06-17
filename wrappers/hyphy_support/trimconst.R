#!/usr/bin/Rscript
library(data.table)
fn = commandArgs(TRUE)[1]
dt = fread(fn, sep = ',', header = TRUE)
dtfil = dt[,which(colSums(dt) %ni% c(0,ncol(dt))), with = FALSE]
write.table(dtfil, file=paste(fn, '.fixed', sep=''), quote=F, sep=',', row.names=F, col.names=T)
