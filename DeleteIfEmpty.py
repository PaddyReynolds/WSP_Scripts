#-------------------------------------------------------------------------------
# Name:        Delete_Empty_Feature_Classes_From_GDB
# Purpose:     To remove empty feature classes from a GDB to streamline GDB
#
# Author:      UKVVK001
#
# Created:     13/06/2019
# Copyright:   (c) UVVK001 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
from arcpy import env

workspace = #GDB Containing Features

#set work space for running script - in this case a GDB
arcpy.env.workspace = workspace

#Make list of data within GDB to run analysis on
fclist = arcpy.ListFeatureClasses()

txt_Path = os.path.dirname(os.path.abspath(workspace))

#Make list of data within GDB to run analysis on
kept = open(os.path.join(txt_Path, "Retained.txt"), "w")
removed = open(os.path.join(txt_Path, "Removed.txt"), "w")


#Loop through list to get count of features and remove any that are empty
arcpy.AddMessage("Removing empty feature classes from GDD")
for fc in fclist:
    name = str(fc)
    count1 = str(arcpy.GetCount_management(fc))
    if count1 == "0":
        removed = open(os.path.join(txt_Path, "Removed.txt"), "w")
        arcpy.AddMessage(name + " had no features so was removed")
        arcpy.Delete_management(fc)
        removed.write(name + '\n')
        removed.close()

    if count1 != "0":
        kept = open(os.path.join(txt_Path, "Retained.txt"), "w")
        kept.write(name + '\n')
        arcpy.AddMessage(name + " has features so was not removed")
        kept.close()



arcpy.AddMessage("Script Complete")