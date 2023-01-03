#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     01/09/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy


inFC = r'\\DCEMA100APP53\Data\National_Polygon_Service\13_GSS\132_GIS\GIS_Data\Geodatabases\National_Polygon_Service_FullSupply.gdb\GEODATA\NPD_FullSupply'
outFC = r'C:\Users\UKPXR011\Desktop\Scripts\NPS_Extract\Scratch.gdb\Titles'
arcpy.env.workspace = r'C:\Users\UKPXR011\Desktop\Scripts\NPS_Extract\Scratch.gdb'
arcpy.env.overwriteOutput = True
where_clause = """ "TITLE_NO" IN ('HD194053','HD103527','HD419675')"""

if arcpy.Exists(outFC):
    arcpy.Delete_management(outFC)

arcpy.Select_analysis(inFC, outFC, where_clause)

print "Done"



