#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      UKPXR011
#
# Created:     24/06/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os

aoi1 = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\Scratch.gdb\AOI'
outPath = "C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Manchester.gdb\\"
workspace = r'\\10.44.252.11\GSS_Data\National_Polygon_Service\13_GSS\132_GIS\GIS_Data\Geodatabases\National_Polygon_Service_June2020_FullSupply.gdb'


arcpy.env.workspace = workspace
features = arcpy.ListFeatureClasses("*")
path = "\\10.44.252.11\GSS_Data\National_Polygon_Service\13_GSS\132_GIS\GIS_Data\Geodatabases\National_Polygon_Service_June2020_FullSupply.gdb\\"
outPath = "C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Manchester.gdb\\"

fc1 = r'\\10.44.252.11\GSS_Data\National_Polygon_Service\13_GSS\132_GIS\GIS_Data\Geodatabases\National_Polygon_Service_June2020_FullSupply.gdb\GEODATA\NPD_June2020_FullSupply'
fc2 = outPath + '\\' + 'MCR_NPS'

arcpy.Clip_analysis(fc1, aoi1, fc2)




