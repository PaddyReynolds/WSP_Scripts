#-------------------------------------------------------------------------------
# Name:        BoR Plot Automation Script
# Purpose:     Automate numbering of BoR plots from South to North
#
# Author:      Kane Russell
#
# Created:     24/05/2019
# Copyright:   (c) UKKXR602 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
import os
import shutil
import datetime

#Date
now = datetime.datetime.now()
Date = now.strftime("%Y%m%d%H%M")

#Set Parameters
fc = arcpy.GetParameterAsText(0)
field_to_update = 'Plot_Number'
field = "Parish"

#Create local GDB & work folders
arcpy.AddMessage("Creating Local Copy")
desktopPath = os.environ.get( "USERPROFILE" ) + "\\Desktop"
os.makedirs(desktopPath + "\\PlotNumberingScratch" + Date)
TempFolder = desktopPath + "\\PlotNumberingScratch" + Date
ScratchGDD = "PlotScratch"
WorkGDD = TempFolder + "\\" + ScratchGDD + ".gdb"
dissolvedPlots = WorkGDD + "\\" + "DissolvedPlots"
arcpy.CreateFileGDB_management(TempFolder,ScratchGDD)

#dissolve plot draft to create parcel list
arcpy.AddMessage("Dissolving Plots to Generate Parcel List to Number Plots")
arcpy.Dissolve_management(fc,dissolvedPlots,field,"",)
fc2 = dissolvedPlots

#Auto Number Plots from South to North
arcpy.AddMessage("Auto Numbering Plots from South to North")
cursor = arcpy.SearchCursor(fc2)
for row1 in cursor:
    parishes = str(row1.getValue(field))
    query = str(field) + " ='" + parishes + "'"
    coords = [[round(i[0],0),round(i[1],0),i[2]] for i in arcpy.da.SearchCursor(fc,['SHAPE@X','SHAPE@Y','OID@'],query)]
    coords.sort(key=lambda k: (k[1],-k[0]), reverse=False)
    order = [i[2] for i in coords]
    d = {k:v for (v,k) in list(enumerate(order))}
    with arcpy.da.UpdateCursor(fc,["OID@",field_to_update],query) as cursor:
        for row in cursor:
            row[1] = int(d[row[0]]+1)
            cursor.updateRow(row)

#Delete superflous data & lockfiles
del(row)
del(row1)
arcpy.Delete_management(dissolvedPlots)

#delete scratch folder
arcpy.AddMessage("Deleting Scratch Folder")
shutil.rmtree(TempFolder)
arcpy.AddMessage("Script Complete")