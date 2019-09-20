#=======================================================
# BCFWA Streamline Networking
#=======================================================
# Search upstream and downstream with the BCFWA
print("Starting........................")
print("bcfwaStreamlineUSDS........................")
tool_exec <- function(in_params, out_params)
{
  #### Load Library for Analysis ####
  if (!requireNamespace("dplyr", quietly = TRUE))
    install.packages("dplyr")
  require(dplyr)
  
  #### Get Input Parameters ####
  input_reaches <- in_params[[1]]
  input_strmnetwork <- in_params[[2]]
  input_indextable <- in_params[[3]]
  input_usds <- in_params[[4]]
  #### Get Input Parameters ####
  output_features <- out_params[[1]]

  
  #### Get Linear Feature IDs for Target Reaches ####
  tr <- arc.open(input_reaches)
  tr_df <- arc.select(tr)
  tlfids <- as.data.frame(tr_df[,"LINEAR_FEATURE_ID"])
  tlfids <- tlfids %>% unlist() %>% as.numeric()
  print(tlfids)
  
  #### Get USDS reaches from index table ###
  print(input_indextable)
  index_tab <- read.csv(input_indextable)
  print(paste0("nrow table: ", nrow(index_tab)))
  # If downstream switch directions
  if(input_usds == "Downstream"){
    print("Working Downstream")
    colnames(index_tab) <- c("usid", "id")
  }
  index_tab_sub <- index_tab[which(index_tab$id %in% tlfids),]
  
  #### Crop out streamnetwork to only include target reaches
  strm <- arc.open(input_strmnetwork)
  #biglist <- paste0("LINEAR_FEATURE_ID IN(", paste(as.character(index_tab_sub$usid), collapse = ","), ")")
  strm_sub <- arc.select(strm) # , where_clause=biglist)
  strm_sub <- strm_sub[which(strm_sub$LINEAR_FEATURE_ID %in% index_tab_sub$usid),]
  print(paste0("Upstream feature count:", nrow(strm_sub)))

  ### Add on Target reach id ###
  strm_sub$target_id <- index_tab_sub$id[match(strm_sub$LINEAR_FEATURE_ID, index_tab_sub$usid)]
  
  #testoutput <- arc.data2sp(strm_sub)
  #plot(testoutput)
  
  arc.write(output_features, strm_sub, overwrite = TRUE)
  
  return(out_params)
 
}
print("Completed........................")

  



# For testing in R only - Skip this
if(FALSE){
  library(arcgisbinding)
  arc.check_product() 
  in_params <- list()
  in_params[[2]] <- "F:/spatial_data_raw/BCFWA/FWA_STREAM_NETWORKS_SP.gdb/SQAM"
  in_params[[1]] <- "F:/delete/Output.gdb/targsrtm"
  in_params[[3]] <- "F:/FWA Network/1_bcfwa_attributes/1_index_upstream_line_to_line_id_tables/SQAM_us_lfid.csv"
  in_params[[4]] <- "Upstream"
  out_params <- list()
  out_params[[1]] <- "F:/delete/Output.gdb/myoutput"
  
} # end of testing section
#======================================================
