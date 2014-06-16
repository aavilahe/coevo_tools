# tabIO.R -- read various types of "tab" files

#cat('loadTab_mfDCA() is hard coded to assume 1000 bootstraps\n', file=stderr())
#cat('loadTab_plmDCA() is hard coded to assume 1000 bootstraps\n', file=stderr())
#cat('loadTab_psicov() is hard coded to assume 1000 bootstraps\n', file=stderr())
#cat('loadTab_hpDCA() is hard coded to assume 1000 bootstraps\n', file=stderr())

loadTab = function(fn, column_labels){
	# Loads output from coevolution wrapper output as data.frames
	tab = read.table(fn, sep='\t')
	colnames(tab) = c('Virus_Column', 'Mammal_Column', column_labels)

	return(tab)
}

fixNAs = function(tab, column_labels){
	# Set the p-value to 1 for scores with NA values
	for(stat in column_labels){
		p_stat = paste('p',stat,sep='_')
		if(p_stat %in% column_labels){
			tab[is.na(tab[,stat]), p_stat] = 1
#			tab[,p_stat] = p.adjust(tab[,p_stat], method='holm') # fwer control (better than bonferroni)
		}
	}
	return(tab)
}

cleanWhats = function(Whats){
	# Set NAs to minimum value in "Whats"
	minWhat = min(Whats, na.rm=TRUE)
	Whats[!is.finite(Whats)] = minWhat
	return(Whats)
}

set_whatCmp = function(whatName, opt_what){
	# Set whether big or small values are better.
	# If looking at Pvalues or Distances (eg. VI) small values indicate coevolution
	
	if(opt_what == 'Pvalue' | opt_what == 'Rank' | whatName == 'VI'){
		return('<')
	}
	return('>')
}

addPemp = function(tab, column_labels){
	# Calculate Pempirical values for scores given in "column_labels"
	# and add them to "tab" data.frame
	rank_these_labels = grep('^p_', column_labels, invert=TRUE, value=TRUE)
	for(label in rank_these_labels){
		flip = (set_whatCmp(label, 'Score') == '<')
		rlabel = paste('r', label, sep='_')
		x = cleanWhats(tab[, label])
		if(flip){
			R = 1 - ecdf(-x)(-x)
		} else {
			R = 1 - ecdf(x)(x) # could also use: rank(x, ties.method='max') / length(x)
		}
		tab[, rlabel] = R
	}
	return(tab)
}

addPnorm = function(tab, column_labels){
	# Calculate Pnormal values for scores give in "column_labels"
	# and add them to "tab" data.frame
	zscore_these_labels = grep('^p_', column_labels, invert=TRUE, value=TRUE)
	for(label in zscore_these_labels){
		flip = (set_whatCmp(label, 'Score') == '<')
		zlabel = paste('z', label, sep='_')
		x = cleanWhats(tab[, label])
		if(flip){
			Z = -scale(x)
		} else {
			Z = scale(x)
		}
		tab[, zlabel] = pnorm(Z, lower.tail=FALSE)
	}
	return(tab)
}

loadTab_infCalc = function(fn, suff=NULL){
	# Load tab output from infCalc
	# after processing with make_tab.py and optionally fix_dummy_pvalues.py
	column_labels = c('Vir_Entropy', 'Mam_Entropy', 'Joint_Entropy',
						'MI', 'VI',
						'MIminh', 'MIj',
						'p_MI', 'p_VI',
						'p_MIminh', 'p_MIj')
	if(!is.null(suff)){
		column_labels = paste(column_labels, suff, sep='_')
	}
	tab = loadTab(fn, column_labels)
	tab = fixNAs(tab, column_labels)
	tab = addPemp(tab, column_labels)
	tab = addPnorm(tab, column_labels)
	return(tab)
}

loadTab_mfDCA = function(fn, suff=NULL){
	# Load tab output from (mean field) DCA package
	# after processing with make_tab.py and optionally fix_dummy_pvalues.py
	column_labels = c('MIw', 'DI', 'p_MIw', 'p_DI')
	if(!is.null(suff)){
		column_labels = paste(column_labels, suff, sep='_')
	}
	tab = loadTab(fn, column_labels)
#	tab[, column_labels[c(3,4)]] = tab[, column_labels[c(3,4)]] / 1000 # hard coded
	tab = fixNAs(tab, column_labels)
	tab = addPemp(tab, column_labels)
	#tab = addPnorm(tab, column_labels[1]) # add zscores for dcaMI only
	tab = addPnorm(tab, column_labels) # add zscores for dcaMI and dcaDI
	return(tab)
}

loadTab_plmDCA = function(fn, suff=NULL){
	# Load tab output from (symmetric) plmDCA package
	# after processing with make_tab.py and optionally fix_dummy_pvalues.py
	column_labels = c('DIplm', 'p_DIplm')
	if(!is.null(suff)){
		column_labels = paste(column_labels, suff, sep='_')
	}
	tab = loadTab(fn, column_labels)
#	tab[ , column_labels[2] ]= tab[, column_labels[2] / 1000 # hard coded
	tab = fixNAs(tab, column_labels)
	tab = addPemp(tab, column_labels)
	return(tab)
}

loadTab_psicov = function(fn, suff=NULL){
	# Load tab output from PSICOV package
	# after processing with make_tab.py and optionally fix_dummy_pvalues.py
	column_labels = c('psicov', 'p_psicov')
	if(!is.null(suff)){
		column_labels = paste(column_labels, suff, sep='_')
	}
	tab = loadTab(fn, column_labels)
#	tab[, column_labels[2]] = tab[, column_labels[2]] / 1000 # hard coded
	tab = fixNAs(tab, column_labels)
	tab = addPemp(tab, column_labels)
	return(tab)
}

loadTab_hpDCA = function(fn, suff=NULL){
	# Load tab output from hpDCA package
	# after processing with make_tab.py and optionally fix_dummy_pvalues.py
	column_labels = c('hpDI', 'p_hpDI')
	if(!is.null(suff)){
		column_labels = paste(column_labels, suff, sep='_')
	}
	tab = loadTab(fn, column_labels)
#	tab[, column_labels[2] ] = tab[, column_labels[2] ] / 1000 # hard coded
	tab = fixNAs(tab, column_labels)
	tab = addPemp(tab, column_labels)
	return(tab)
}

loadTab_dists = function(fn, DistStr='Distance'){
	column_labels = c(DistStr)
	tab = loadTab(fn, column_labels)
	return(tab)
}



