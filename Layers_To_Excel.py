#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     23/09/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env, mapping
import os

mydir = r'\\10.44.252.11\GSS_Data\62240842-HS2_Phase_2A\13_GSS\132_GIS\ArcGIS\MXDforPublishing'
mxdList = []
LayersList = []

for file in os.listdir(mydir):
    if file.endswith(".mxd"):
        mxdList.append(os.path.join(mydir, file))

for WebMap in mxdList:

    mxd = mapping.MapDocument(WebMap)
    lyrs = mapping.ListLayers(mxd)
    print WebMap

    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.supports("DATASOURCE"):
            source = lyr.dataSource
            LayersList.append(source)


with open(r"\\10.44.252.11\GSS_Data\62240842-HS2_Phase_2A\13_GSS\132_GIS\ArcGIS\MXDforPublishing\Layers_QC.txt", 'w') as f:
    for item in LayersList:
        f.write("%s\n" % item)

