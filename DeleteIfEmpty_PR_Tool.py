#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     18/12/2019
# Copyright:   (c) UKPXR011 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
from arcpy import env

workspace = arcpy.GetParameterAsText(0)
delete = arcpy.GetParameterAsText(1)
#set work space for running script - in this case a GDB
arcpy.env.workspace = workspace

#Make list of data within GDB to run analysis on
fclist = arcpy.ListFeatureClasses()

txt_Path = os.path.dirname(os.path.abspath(workspace))

#Make list of data within GDB to run analysis on
kept = []
removed = []


#Loop through list to get count of features and remove any that are empty
arcpy.AddMessage("Removing empty feature classes from GDD")
for fc in fclist:
    name = str(fc)
    count1 = str(arcpy.GetCount_management(fc))
    if count1 == "0":
        removed.append(fc)
        if str(delete) == 'true':
            arcpy.Delete_management(fc)
            arcpy.AddMessage(name + " had no features so was removed")
        else:
            arcpy.AddMessage(name + " has no featuers")


    if count1 != "0":
        kept.append(fc)
        arcpy.AddMessage(name + " has features so was not removed")


with open(os.path.join(txt_Path, "Retained.txt"), "w") as f:
    for item in kept:
        f.write("%s\n" % item)

with open(os.path.join(txt_Path, "Removed.txt"), "w") as f:
    for item in removed:
        f.write("%s\n" % item)


arcpy.AddMessage("Script Complete")
