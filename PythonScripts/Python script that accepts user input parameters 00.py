####################################################
# This Python toolbox script is provided as an example
# to demonstrate a simple script that creates a buffer
# around roads and calculates the total length of stream
# by stream order within the buffered distance.
####################################################

# Import system modules
import arcpy
from arcpy import env
 
# Set environment settings
env.workspace = "C:/Users/mbayly/Desktop/Projects/PROPOSALS/7300-08.00 Cumulative Effects Hazard Calculator Tool/Proposal/Sample Code/r-BCFWA-network/sampledata.gdb"
arcpy.env.overwriteOutput = True
 
# Set local variables
inRoads = "roads"
outBuffer = "roads_buff100"
bufferDistance = "100 meters"
inStreams = "strm_network"
outClip = "strm_clip_out"
outStatsTable = "stats_out"
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