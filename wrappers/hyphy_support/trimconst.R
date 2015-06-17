#!/usr/bin/Rscript
library(data.table)
fn = commandArgs(TRUE)[1]
dt = fread(fn, sep = ',', header = FALSE)
the_headers = as.character(0:(ncol(dt) - 1))
setnames(dt, the_headers)
dtfil = dt[,which(colSums(dt) %ni% c(0,nrow(dt))), with = FALSE]
write.table(dtfil, file=paste(fn, '.fixed', sep=''), quote=F, sep=',', row.names=F, col.names=T)
