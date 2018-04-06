list_of_uars <- lapply(1:7, function(x) runif(5000))
big_set <- do.call('cbind',list_of_uars)

apply(big_set, 1, function(row) {
	
})