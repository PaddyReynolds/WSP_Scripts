#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     06/01/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
import shutil
import csv
import win32com.client as win32
from datetime import datetime
arcpy.env.overwriteOutput = True

#Date
startTime = datetime.datetime.now()

#Create work space
desktopPath = r'C:\Users\UKPXR011\Desktop\Scratch\Historical_GDB'

#Choose Work Database To Run QC Check
SDE_Geodatabase = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde"

WorkFolder = desktopPath
workGDB = desktopPath +"\\Historical.gdb"

arcpy.env.workspace = SDE_Geodatabase
limit_Layer = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde\ACCESSLICENCES_H1"

testFeature = workGDB +"\\Test"

print "Trying"
arcpy.CopyFeatures_management(limit_Layer, testFeature)
print "Done"


print(datetime.datetime.now() - startTime)