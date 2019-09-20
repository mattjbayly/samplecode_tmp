#=======================================================
# BCFWA Stream Gradient
#=======================================================
# Print a Plot of the stream gradient
print("Starting........................")


bcfwa01_getStreamLineElevEndpoints <- function(strm.df = NA,
                                               geom.length.colname = "GEOMETRY_Length",
                                               linear.feature.id.colname = "LINEAR_FEATURE_ID"
){

  # Build empty matrix to build onto
  coord_list <- matrix(NA, nrow(strm.df), 4)
  # temp id col
  ids <- as.data.frame(strm.df[,linear.feature.id.colname])[,1]
  lengths <- as.data.frame(strm.df[,geom.length.colname])[,1]
  
  # Loop through each individual line segment
  for(i in 1:dim(strm.df)[1]){
    these_cords <- st_coordinates(strm.df[i,])
    upper <- max(these_cords[,"Z"], na.rm=TRUE)
    lower <- min(these_cords[,"Z"], na.rm=TRUE)
    
    #id <- strm.df$LINEAR_FEATURE_ID[i]
    id <- ids[i]
    length <- lengths[i]
    
    coord_list[i,] <- c(id, lower, upper, length)
    if(i %% 1000 == 0){
      print(paste0(round(i/nrow(strm.df), 3)*100, " % complete"))
    }
  }
  print("Completed elevation line segment endoint calculations")
  #-----------------------------------------------------
  
  # Calculate gradient from elevation drop and stream line length
  elev.df <- data.frame(coord_list)
  colnames(elev.df) <- c("id", "lower", "upper", "length")
  elev.df$elev_drop <- elev.df$upper - elev.df$lower 
  # Calculate Stream Gradient
  elev.df$gradient <- elev.df$elev_drop/elev.df$length
  
  # Look at gradient summary calculations
  # Make sure stream is not going uphill
  #hist(elev.df$gradient, xlim=c(0,1), breaks=1000, col="blue", main="Gradient Summary")
  
  #Return df to user 
  return(elev.df)
  
}







tool_exec <- function(in_params, out_params)
{
  #### Load Library for Analysis ####
  if (!requireNamespace("dplyr", quietly = TRUE))
    install.packages("dplyr")
  if (!requireNamespace("ggplot2", quietly = TRUE))
    install.packages("ggplot2")
  if (!requireNamespace("sf", quietly = TRUE))
    install.packages("sf")
  require(dplyr); require(ggplot2); require(sf)
  print("bcfwaStreamGradient........................")
  
  #### Get Input Parameters ####
  input_line <- in_params[[1]]

  #### Get Linear Feature IDs for Target Reaches ####
  tr <- arc.open(input_line)
  tr_df <- arc.select(tr)
  
  #### Conver to sf object and extract geometry
  strm <- arc.shape2sf(arc.shape(tr_df))
  strm <- st_sf(strm)
  strm$GEOMETRY_Length <- tr_df$GEOMETRY_Length
  strm$LINEAR_FEATURE_ID <- tr_df$LINEAR_FEATURE_ID
  strm$GEOMETRY_Length <- tr_df$GEOMETRY_Length
  print("Getting elevation end points")
  elev <- bcfwa01_getStreamLineElevEndpoints(strm.df = strm)
  
  # Merge elev data on 
  strm_elev <- merge(strm,elev, by.x="LINEAR_FEATURE_ID", by.y="id", all.x=TRUE)
  # re-order based on elev
  strm_ord <- strm_elev %>% arrange(-upper)
  strm_ord$tot_length <- cumsum(strm_ord$GEOMETRY_Length)
  
  #plot(strm_ord$tot_length, strm_ord$upper, type="l")
  
  g <- ggplot(data=strm_ord, aes(x=tot_length, y=upper)) +
    geom_line() + geom_point()+
    xlab("DISTANCE DOWNSTREAM (m)") + ylab("ELEVATION (m)") +
    theme_minimal()
  print("Printing plot")
  print(g)
  return(out_params)
  
}
print("Completed........................")





# For testing in R only - Skip this
if(FALSE){
  library(arcgisbinding)
  arc.check_product() 
  in_params <- list()
  in_params[[1]] <- "C:/Users/mbayly/Desktop/Projects/PROPOSALS/7300-08.00 Cumulative Effects Hazard Calculator Tool/Proposal/Sample Code/r-BCFWA-network/sampledata.gdb/strm_grd"

} # end of testing section
#======================================================
