#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     17/10/2019
# Copyright:   (c) UKPXR011 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

fc = 'C:\Users\UKPXR011\Desktop\Street_View\Scratch.gdb\NEW_LOP_ROAD_POINTS'
fields = "'X'"

print (arcpy.ListFields(fc))


with arcpy.da.UpdateCursor(fc,fields) as cursor:

    for row in cursor:

        arcpy.PointGeometry(row.firstPoint,row.spatialReference).projectAs(arcpy.SpatialReference(3857)).firstPoint.X

        cursor.updateRow(row)

