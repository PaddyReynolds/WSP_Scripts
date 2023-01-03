#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     20/05/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, os

# The map with the bookmarks
mxd = arcpy.mapping.MapDocument(r"C:\Users\UKPXR011\Desktop\Current Work\2A\Scratch\A102_068\LAP_A102_068_C02_.mxd")

# The output feature class to be created -
# This feature class will store the bookmarks as features
outFC = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Scratch\A102_068\A102_068.gdb\Bookmarks'

# A template feature class that contains the attribute schema
# Including a "Name" field to store the bookmark name
template = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Scratch\A102_068\A102_068.gdb\Template'

if arcpy.Exists(outFC):
    arcpy.Delete_management(outFC)
arcpy.CreateFeatureclass_management(os.path.dirname(outFC),
                                    os.path.basename(outFC),
                                    "POLYGON", template,
                                    spatial_reference=template)

cur = arcpy.da.InsertCursor(outFC, ["SHAPE@", "Name"])
array = arcpy.Array()
for bkmk in arcpy.mapping.ListBookmarks(mxd):
    array.add(arcpy.Point(bkmk.extent.XMin, bkmk.extent.YMin))
    array.add(arcpy.Point(bkmk.extent.XMin, bkmk.extent.YMax))
    array.add(arcpy.Point(bkmk.extent.XMax, bkmk.extent.YMax))
    array.add(arcpy.Point(bkmk.extent.XMax, bkmk.extent.YMin))
    # To close the polygon, add the first point again
    array.add(arcpy.Point(bkmk.extent.XMin, bkmk.extent.YMin))
    cur.insertRow([arcpy.Polygon(array), bkmk.name])
    array.removeAll()