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
import arcpy
import math

fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\A101_071\A101_071.gdb\newnpsextents_Combined'


def iScale(xMin, yMin, xMax, yMax):
		scaleRange = [1250, 2500, 5000, 7500, 10000]
		diagonal = float(math.sqrt((xMax-xMin)*(xMax-xMin) + (yMax-yMin)*(yMax-yMin)))
		initialScale = 10000
		for scale in scaleRange:
			xTent = ((scale/100)*int(28))
			if (diagonal < xTent):
				initialScale = scale
				break
		return initialScale



with arcpy.da.UpdateCursor(fc1, ["SHAPE@", "NPNo", "Scale"]) as updateRows:

    for updateRow in updateRows:
		extent = updateRow[0].extent
		array = arcpy.Array([arcpy.Point(extent.XMin, extent.YMin), arcpy.Point(extent.XMax, extent.YMin), arcpy.Point(extent.XMax, extent.YMax), arcpy.Point(extent.XMin, extent.YMax)])
		polygon = arcpy.Polygon(array)
		Intial_Scale = iScale((extent.XMin), (extent.YMin), (extent.XMax), (extent.YMax))
		updateRow[2] = float(Intial_Scale)
		updateRows.updateRow(updateRow)
    del updateRows


