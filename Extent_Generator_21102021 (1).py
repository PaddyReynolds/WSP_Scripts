#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     21/10/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

with arcpy.da.UpdateCursor(fc6, ["SHAPE@", "Notice_Plan_Input_Notice_Number", "Scale"]) as updateRows:

    for updateRow in updateRows:
        extent = updateRow[0].extent
        #LAA_ID = ("{0}".format(row[1]))
            # Create a polygon geometry
        array = arcpy.Array([arcpy.Point(extent.XMin, extent.YMin), arcpy.Point(extent.XMax, extent.YMin),
                                 arcpy.Point(extent.XMax, extent.YMax), arcpy.Point(extent.XMin, extent.YMax)])
        polygon = arcpy.Polygon(array)
        polygon_area = float(polygon.area)
        if polygon_area < 100000.00: #140767.95:
            Intial_Scale = '1250'
            updateRow[2] = Intial_Scale
        elif 100000.01 < polygon_area < 350000.00:
            Intial_Scale = '2500'
            updateRow[2] = Intial_Scale
        elif 350000.01 < polygon_area < 1800000.00:
            Intial_Scale = '5000'
            updateRow[2] = Intial_Scale
        elif 1800000.01 < polygon_area < 4500000.00:
            Intial_Scale = '7500'
            updateRow[2] = Intial_Scale
        else:
            Intial_Scale = '10000'
            updateRow[2] = Intial_Scale

        updateRows.updateRow(updateRow)

del updateRows
