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
import datetime
arcpy.env.overwriteOutput = True
Lnumbers = []
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

print "Trying"
with arcpy.da.SearchCursor(limit_Layer,['LicenceID']) as cursor:
    for row in cursor:
        Lnumbers.append(str(row[0]))

print "Done"
print Lnumbers

LnumbersClean = list(dict.fromkeys(Lnumbers))
LnumbersClean.sort()

LnumbersRangeTemp = list(range(1, 90000))
LnumbersRange =  list("L" + str(i) for i in LnumbersRangeTemp)
LnumbersAvalible = [x for x in LnumbersRange if x not in LnumbersClean]

with open(os.path.join(desktopPath, "AvalibleLnumbers_15032020.txt"), "w") as f:
    for item in LnumbersAvalible:
        f.write("%s\n" % item)

print(datetime.datetime.now() - startTime)