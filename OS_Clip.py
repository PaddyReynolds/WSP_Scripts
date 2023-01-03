#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     05/11/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

workspace = r'C:\Users\UKPXR011\Desktop\Current Work\2b\OS\P30\ORDSU_MasterMapTopo_202210\ORDSU_MasterMapTopo_202210.gdb'
OS_GDB = r'C:\Users\UKPXR011\Desktop\Current Work\2b\OS\P30\P30_OS.gdb\\'
AOI = r'C:\Users\UKPXR011\Desktop\Current Work\2b\OS\2B_OS\P28_HS2B_Manchester\Trimmed_OS.gdb\AOI'
arcpy.env.workspace = workspace
features = arcpy.ListFeatureClasses("*")

print features
pathway = r'C:\\Users\\UKPXR011\\Desktop\\Current Work\\2b\\OS\\P30\\ORDSU_MasterMapTopo_202210\\ORDSU_MasterMapTopo_202210.gdb\\'

for i in features:
    # Define output feature class location
    fc = OS_GDB +'\\'+ i
    # Define Selection criteria
    infc = pathway + str(i)
    print infc
    layer = str(i)+"_Layer"
    arcpy.MakeFeatureLayer_management(infc, layer)
    Selection = arcpy.SelectLayerByLocation_management(layer, "INTERSECT",AOI)
    # Define output selection and fc
    arcpy.CopyFeatures_management(Selection, fc)

