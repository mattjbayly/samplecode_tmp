####################################################
# Create revised road layer
# Subset of FTEN and DRA
####################################################

import arcpy
import os
from arcpy import env

# Set environment settings
env.workspace = "F:/Projects/1412 IMA Reports/WSEP_T1/01_Watershed Intersect with layers/WatershedIntersect.gdb"
# Directories
dir_sheds = "F:/Projects/00_Watershed Boundaries/"
dir_raw = "F:/Projects/WSEP Tier 1 Raw Data/"
dir_ften = "F:/Projects/01_Watershed Intersect with layers/Road Adjustments"

####################################################
# Set of paths - to target watersheds and management areas
f_sheds = dir_sheds + "Watersheds.shp"

########################################
# Check Spatial Projections
# Load custom intersect helper function ------------
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

layer1s = "dra_dgtl_road_atlas"
layer2s = dir_ften + "/FTENRoadSegments.shp"
projFunc(layer1s=layer1s, layer2s=layer2s)

# Reproject and intersect function ------------------------------
def intersectFunction(instring, outstring):
    in_features1 = instring
    in_features2 = f_sheds
    in_features = [in_features1, in_features2]
    proj1 = arcpy.Describe(in_features1).spatialReference.name
    proj2 = arcpy.Describe(in_features2).spatialReference.name
    print(proj1)
    print(proj2)
    # Re Projection Needed
    if "Albers" not in proj1:
        print("Need to project")
        output_feature_class = "tmp_proj"
        print(proj2)
        print(proj1)
        out_coordinate_system = arcpy.Describe(in_features2).spatialReference
        print(out_coordinate_system)
        arcpy.Project_management(in_features1, output_feature_class, out_coordinate_system)
        print("Spatial Projection Complete")
        in_features1 = output_feature_class # Overwrite
        in_features = [in_features1, in_features2]
    # End of repr
    # Run Intersect
    out_feature_class = outstring
    arcpy.Intersect_analysis(in_features, out_feature_class)
    # Delete tmp layer
    arcpy.Delete_management("tmp_proj", "tmp_proj")
    print("Function Complete")

# FTEN Road Segments  ------------------------------
instring = dir_ften + "/FTENRoadSegments.shp"
outstring = "FTENRoadSegments"
intersectFunction(instring, outstring)

# MergeLayers Togehter  ------------------------------
merge1 = "FTENRoadSegments"
merge2 = "dra_dgtl_road_atlas"
arcpy.Merge_management([merge1, merge2], "RoadsMergeDRAFTEN")

# Add new field for buffer field width  ------------
# No highways intersect FSWs so assume all lanes are 5 m width
# Create new road field for 5 m buffer times lane width
arcpy.AddField_management("RoadsMergeDRAFTEN", "buffdist", "LONG", 9, field_is_nullable="NULLABLE")
arcpy.CalculateField_management("RoadsMergeDRAFTEN", "buffdist", "!TOTAL_NUMBER_OF_LANES! * 5")
# Set default NULL to 5,
with arcpy.da.UpdateCursor("RoadsMergeDRAFTEN", ["buffdist"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[0] = 5
            cursor.updateRow(row)
print("Processing complete")
# Generate buffer
arcpy.Buffer_analysis("RoadsMergeDRAFTEN", "RoadsMergeDRAFTEN_poly", "buffdist", "FULL", "ROUND", "ALL")
#-----------------------
