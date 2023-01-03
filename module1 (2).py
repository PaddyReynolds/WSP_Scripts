#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     11/11/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import mapping
import os
import shutil
import csv
import string
import ConversionUtils
import math
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(27700)

#Input features

Folder_location = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\SoS'
Input_Features = r'C:\Users\UKPXR011\Documents\ArcGIS\FeatureServiceLocalEdits\HS2_Phase1_South_HS2_Phase2a_Feature\fs27C562E2B2334ACEA16186D700EAE7B2.gdb\LandAcquisitionParcels'
templateMXD = r'C:\Users\UKPXR011\Desktop\Scripts\Noitce Plans\SoS\SoS_Template.mxd'
LAPS = ['103682','103681']
x = "','".join(LAPS)
LAANum  = 'A101_001'
LAPquery = "LAPID IN('"+ x +"')"
newFolder = Folder_location + "\\" + LAANum  + "_SoS"
newMxd = newFolder + "\\" + LAANum  + "_SoS.mxd"
newGDB = LAANum  + ".gdb"
newPath =newFolder + "\\" + newGDB
Fields1 = [('Revision','DOUBLE'),('DocNumber','STRING'),('Scale','DOUBLE'),('Export_ID','SHORT')]


def MultipleAddFields(FeatureToAdd,Fields):
#fields should be held as pairs, eg [('Study_Area','TEXT'),('Area','Double')]
    for a,b in Fields:
        arcpy.AddField_management(FeatureToAdd,a,b,'','','','')

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



'''
if os.path.isdir(newFolder) is False:
    os.mkdir(newFolder)
    print 'Folder '+ LAANum  + ' Created'

else:
    print 'Folder Already Exists'

if os.path.isfile(newMxd):
    print 'MXD Already Exists'


else:

    shutil.copy(templateMXD,newMxd)
    print 'MXD created'

if arcpy.Exists(newPath) is False:

    arcpy.management.CreateFileGDB(newFolder, newGDB)
    arcpy.env.workspace = newPath
    print 'GDB Created'


else:

    print 'GDB Already Exists'
    arcpy.env.workspace = newPath

'''

#Make a DDP and scale
SoS_Lap = newFolder+ "//" + newGDB + "//"+"SoS_Laps"
DDP = newFolder+ "//" + newGDB + "//"+"DDP"

arcpy.analysis.Select(Input_Features, SoS_Lap,LAPquery)
arcpy.Dissolve_management(SoS_Lap,DDP,"LAAID")
MultipleAddFields(DDP,Fields1)


with arcpy.da.UpdateCursor(DDP, ["SHAPE@", "Scale"]) as updateRows:

    for updateRow in updateRows:
		extent = updateRow[0].extent
		array = arcpy.Array([arcpy.Point(extent.XMin, extent.YMin), arcpy.Point(extent.XMax, extent.YMin), arcpy.Point(extent.XMax, extent.YMax), arcpy.Point(extent.XMin, extent.YMax)])
		polygon = arcpy.Polygon(array)
		Intial_Scale = iScale((extent.XMin), (extent.YMin), (extent.XMax), (extent.YMax))
		updateRow[1] = float(Intial_Scale)
		updateRows.updateRow(updateRow)


    del updateRows


#Repoint layers and make DDP



#Export Plans
