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
#Empty List to hold Lnumbers
Lnumbers = []
#Date
startTime = datetime.datetime.now()

#CSet the workspace
desktopPath = r'C:\Users\UKPXR011\Desktop\Scratch\Historical_GDB'

#set the environment
SDE_Geodatabase = r"Database Connections\HS2-Phase2A-Manchester-GSS.sde"
arcpy.env.workspace = SDE_Geodatabase

#Set the GDB
WorkFolder = desktopPath
workGDB = desktopPath +"\\Historical.gdb"

#Set the layer of the historical Archive
LAPS = r"Database Connections\HS2-Phase2A-Manchester-GSS.sde\LANDACQUISITIONPARCELS_H2"

print "Accesling Archive"

#SearchCursor for Licence ID and append to a list
with arcpy.da.SearchCursor(LAPS,['LAPID']) as cursor:
    for row in cursor:

        if row is None:
            pass

        else:
            Lnumbers.append(row[0])


print "List of Lnumbers Created"

#Write the Lnumbers to a Dictionary and then back to a list to remove duplicates
Lnumbers = list(dict.fromkeys(Lnumbers))
#Sort the List smallest to Larges
Lnumbers.sort()

#Create a list of Lnumbers raninging from 1 to 90000 and append L to the front of every number
LnumbersRange =  list(range(100001, 900000))

#Check if Lnumber is in the archive list, if it is then remove it
Lnumbers = [x for x in LnumbersRange if x not in Lnumbers]

#Open a text document and write the list to it
with open(os.path.join(desktopPath, "LAP_IDS.txt"), "w") as f:
    for item in Lnumbers:
        f.write("%s\n" % item)

print(datetime.datetime.now() - startTime)