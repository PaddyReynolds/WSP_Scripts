#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     11/01/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
from arcpy import mapping


mxd = mapping.MapDocument(r"\\10.44.252.11\\GSS_Data\\62240842-HS2_Phase_2A\\13_GSS\\132_GIS\\ArcGIS\\MXDforPublishing\\HS2p2A_WSP_LandOwnershipAndHMLR.mxd")
lyrs = mapping.ListLayers(mxd)
new_Path = r"\\10.44.252.11\GSS_Data\62240842-HS2_Phase_2A\13_GSS\132_GIS\GIS_Data\Geodatabases\Replication_for_Web_Publishing\HS2p2A_1wayReplicaForWebPublishing_2021.gdb"

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DATASOURCE"):
        source = lyr.dataSource
        Old = lyr.workspacePath
        if 'STATUTORY_PROCESSES' in source:
            lyr.findAndReplaceWorkspacePath(Old, new_Path, False)
            print lyr.dataSource
    mxd.save()
