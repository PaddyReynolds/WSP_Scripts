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

workspace = r'C:\Users\UKPXR011\Desktop\Current Work\2b\Scratch\2DE01-INT-005344\2PT27-MWJ-GI-GDD-M000-000003\2PT27-MWJ-GI-GDD-M000-000003_P02\AP02.gdb'

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
        arcpy.AddMessage(name + " had no features so was removed")
        #arcpy.Delete_management(fc)


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
