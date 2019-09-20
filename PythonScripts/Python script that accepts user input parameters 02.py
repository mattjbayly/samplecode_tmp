####################################################
# Generate spatial summaries across watersheds or 
# management units for
# - Stream Crossing Density
# - Road Development on H60 Line
####################################################

import arcpy
import os
from arcpy import env

# Set environment settings for your machine
env.workspace = "F:/Projects/1412 IMA Reports/WSEP_T1/01_Watershed Intersect with layers/WatershedIntersect.gdb"
# Project Data Directories
dir_sheds = "F:/Projects/1412 IMA Reports/WSEP_T1/00_Watershed Boundaries/"
dir_raw = "F:/Projects/1412 IMA Reports/WSEP Tier 1 Raw Data/"
dir_ften = "F:/Projects/1412 IMA Reports/WSEP_T1/01_Watershed Intersect with layers/Road Adjustments"
dir_h60 = "F:/Projects/1412 IMA Reports/WSEP_T1/02_Watershed DEM analysis/03_ELEV_H60/"
dir_h60_out = "F:/Projects/1412 IMA Reports/WSEP_T1/02_Watershed DEM analysis/H60Merge/"
dir_slp60 = "F:/Projects/1412 IMA Reports/WSEP_T1/02_Watershed DEM analysis/04_SLOPE_60PCT/"
dir_slp60_out = "F:/Projects/1412 IMA Reports/WSEP_T1/02_Watershed DEM analysis/SLP60Merge/"


####################################################
# Directory to target watersheds
f_sheds = dir_sheds + "Watersheds.shp"

####################################################
# Check projections with custom Intersect Function ------------------------------
def projFunc(layer1s, layer2s):
    in_features1 = layer1s
    in_features2 = layer2s
    proj1 = arcpy.Describe(in_features1).spatialReference.name
    proj2 = arcpy.Describe(in_features2).spatialReference.name
    print(proj1)
    print(proj2)
    # Re Projection Needed
    if "Albers" not in proj1:
        print("Need to project")


#----------------------------------------------------------
# Portion of streams logged
# Extract relevant features from Tantalis tenures layers
tantalis = "TA_CRT_SVW_polygon"
outfile = "tmp_layer"
whereClause = "TEN_PURPOS IN ('AGRICULTURE', 'TRANSPORTATION', 'INDUSTRIAL', 'QUARRYING', 'RESIDENTIAL')"
arcpy.Select_analysis(tantalis, outfile, whereClause)
arcpy.Dissolve_management("tmp_layer", "tmp_layer2")

# Add consolidated cutblocks to disturbance layer
arcpy.Union_analysis(["tmp_layer2", "Consolidated_Cutblocks"], "tmp_layer3")
arcpy.Dissolve_management("tmp_layer3", "tmp_layer4")

# Add VRI Forest disturbance 
# [[OPENING_IND = ‘Y1’]] OR
# [[OPENING_ID is not 0 or is not null]] OR
# [[HARVEST_DATE is not null]] OR
# [[EARLIEST_NONLOGGING_DIST_TYPE is not 0]]
where_clause = '("OPENING_IND" = \'Y\') OR ("OPENING_ID" > 0) OR ("HARVEST_DATE" IS NOT NULL) OR ("EARLIEST_NONLOGGING_DIST_TYPE" IS NOT NULL)'
# Execute Select
arcpy.Select_analysis("VEG_COMP_LYR_R1_POLY", "tmp_layer5_VRIdist", where_clause)
arcpy.Union_analysis(["tmp_layer5_VRIdist", "tmp_layer4"], "tmp_layer6")
# Make total human disturbance layer
arcpy.Dissolve_management("tmp_layer6", "DisturbedForestsAll")
env.workspace = "F:/Projects/1412 IMA Reports/WSEP_T1/01_Watershed Intersect with layers/WatershedIntersect.gdb"

# Intersect disturbance layer with stream lines to calculate total portion of streams logged.
arcpy.Intersect_analysis(["DisturbedForestsAll","FWA_ROUTES_SP"], out_feature_class="WSEPStreamsLogged", join_attributes="", cluster_tolerance=1.5, output_type="LINE")


# Stream-road crossing ------------------------------
layer1s = "RoadsMergeDRAFTEN"
layer2s = "FWA_ROUTES_SP"
projFunc(layer1s=layer1s, layer2s=layer2s)
arcpy.Intersect_analysis(["RoadsMergeDRAFTEN","FWA_ROUTES_SP"], out_feature_class="WSEPStreamCross", join_attributes="", cluster_tolerance=1.5, output_type="POINT")


# Road Density 100m stream ------------------------------
layer1s = "RoadsMergeDRAFTEN"
layer2s = "FWA_ROUTES_SP"
# Buffer stream to 100m
arcpy.Buffer_analysis("FWA_ROUTES_SP", "FWA_ROUTES_SP_100mbuff", 100, "FULL", "ROUND", "ALL")
# Intersect Road Layer with 100m buffer
arcpy.Intersect_analysis(["FWA_ROUTES_SP_100mbuff","RoadsMergeDRAFTEN"], out_feature_class="RoadsMergeDRAFTEN_100mstrm", join_attributes="", output_type="LINE")


# Road Density Above H60 Line ------------------------------
arcpy.env.workspace = dir_h60  #change this  
shplist =  arcpy.ListFeatureClasses('*.shp')  
out = os.path.join(dir_h60_out, 'Merged_H60.shp')
arcpy.Merge_management(shplist, out)
# Subset to only above H60
H60_above = dir_h60_out + "/Merged_H60_above.shp"
whereClause = "layer > 1" 
arcpy.Select_analysis(os.path.join(dir_h60_out, 'Merged_H60.shp'), H60_above, whereClause)
# Dissolve and merge Merged_H60_above
H60_above_diss = dir_h60_out + "/Merged_H60_above_diss.shp"
arcpy.Dissolve_management(H60_above, H60_above_diss)


# Repeat intersect for road above H60
projFunc(layer1s=H60_above_diss, layer2s="RoadsMergeDRAFTEN")
out_coordinate_system = arcpy.Describe("RoadsMergeDRAFTEN").spatialReference
to_reproject = os.path.join(dir_h60_out, 'Merged_H60_above_diss.shp')
output_feature_class = os.path.join(dir_h60_out, 'Merged_H60_above_prj.shp')
arcpy.Project_management(to_reproject, output_feature_class, out_coordinate_system)

h60int = os.path.join(dir_h60_out, 'Merged_H60_above_prj.shp')
arcpy.Intersect_analysis([h60int,"RoadsMergeDRAFTEN"], out_feature_class="RoadsMergeDRAFTEN_H60", join_attributes="", output_type="LINE")


# Road Density On Unstable Slopes ------------------------------
arcpy.env.workspace = dir_slp60  #change this  
shplist =  arcpy.ListFeatureClasses('*.shp')  
out = os.path.join(dir_slp60_out, 'Merged_SLP60.shp')
arcpy.Merge_management(shplist, out)
# Subset to only slope above 60 PCT
slp60_above = dir_slp60_out + "/Merged_SLP60_above.shp"
whereClause = "layer > 1" 
arcpy.Select_analysis(os.path.join(dir_slp60_out, 'Merged_SLP60.shp'), slp60_above, whereClause)
# Repeat intersect for road above H60
projFunc(layer1s=slp60_above, layer2s="RoadsMergeDRAFTEN")
out_coordinate_system = arcpy.Describe("RoadsMergeDRAFTEN").spatialReference
to_reproject = os.path.join(dir_slp60_out, 'Merged_SLP60_above.shp')
output_feature_class = os.path.join(dir_slp60_out, 'Merged_SLP60_above_prj.shp')
arcpy.Project_management(to_reproject, output_feature_class, out_coordinate_system)
# Intersect
h60int = os.path.join(dir_slp60_out, 'Merged_SLP60_above_prj.shp')
arcpy.Intersect_analysis([h60int,"RoadsMergeDRAFTEN"], out_feature_class="RoadsMergeDRAFTEN_SLP60", join_attributes="", output_type="LINE")


# Logging on steep slopes ------------------------------
# Intersect
h60int = os.path.join(dir_slp60_out, 'Merged_SLP60_above_prj.shp')
arcpy.Intersect_analysis([h60int,"WSEPStreamsLogged"], out_feature_class="WSEPStreamsLogged_SLP60", join_attributes="", output_type="LINE")

# Redo with Canadain Soil Map SLC
arcpy.Intersect_analysis(["BC_Soil_Surveys_60pct","WSEPStreamsLogged"], out_feature_class="WSEPStreamsLogged_SLP60_SLC", join_attributes="", output_type="LINE")

print("Complete")
#-------------------------------------------------------
