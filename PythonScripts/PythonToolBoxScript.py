####################################################
# This Python toolbox script is provided as an example
# to demonstrate a simple script that creates a buffer
# around roads and calculates the total length of stream
# by stream order within the buffered distance.
####################################################

inRoads = arcpy.GetParameterAsText(0)
inStreams = arcpy.GetParameterAsText(1)
bufferDistance_val = arcpy.GetParameterAsText(2)
outStatsTable = arcpy.GetParameterAsText(3)

# Set additional variables
outBuffer = "roads_buff100"
bufferDistance = bufferDistance_val + " meters"
outClip = "strm_clip_out"
summaryField = "STREAM_ORDER"
statsFields = [["Shape_Length", "SUM"]]
 
# Buffer to get a buffer of major roads
arcpy.Buffer_analysis(inRoads, outBuffer, bufferDistance, dissolve_option = "ALL")
 
# Clip using the buffer output to get a clipped feature class
#  of streamlines
arcpy.Clip_analysis(inStreams, outBuffer, outClip)
 
# Execute Statistics_analysis to get a summary of the total length of stream (by stream order)
#	within 100 m of the road network
arcpy.Statistics_analysis(outClip, outStatsTable, statsFields, summaryField)