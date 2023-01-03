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
from arcpy import env

#set work space for running script - in this case a GDB
arcpy.env.workspace = r'C:\Users\UKPXR011\Desktop\Current Work\2b\AP2\CLS\2DE01-INT-005462\AP2 Full Engineering\2PT27-MWJ-GI-GDD-M000-000003_P03\2PT27-MWJ-GI-GDD-M000-000003_P03\AP02.gdb'

GDB = r'C:\Users\UKPXR011\Desktop\Current Work\2b\AP2\CLS\2DE01-INT-005462\AP2 Full Engineering\2PT27-MWJ-GI-GDD-M000-000003_P03\2PT27-MWJ-GI-GDD-M000-000003_P03\AP02.gdb'

#Make list of data within GDB to run analysis on
fclist = arcpy.ListFeatureClasses('*')

print fclist

#Loop through list to get count of features and remove any that are empty
arcpy.AddMessage("Removing empty feature classes from GDD")
for fc in fclist:
    count1 = str(arcpy.GetCount_management(fc))
    if count1 == "0":
        name = str(fc)
        arcpy.AddMessage(name + " had no features so was removed")
        arcpy.Delete_management(fc)

arcpy.AddMessage("Script Complete!")
