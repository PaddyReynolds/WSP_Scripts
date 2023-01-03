#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     22/01/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy


fc1 = r'C:\Users\UKPXR011\Desktop\Scripts\Relate_Checker\Relates.gdb\STATUTORY_PROCESSES\relLAA_LAPs'
fc2 = r'C:\Users\UKPXR011\Desktop\Scripts\Relate_Checker\Relates.gdb\STATUTORY_PROCESSES\LAA'
fc3 = r'C:\Users\UKPXR011\Desktop\Scripts\Relate_Checker\Relates.gdb\STATUTORY_PROCESSES\LandAcquisitionParcels'

#List of LAP Global IDS and LRTYPE
LAP = []
LAA = []
Relates =[]
#search cursor through LAA saving global ID and LRTYPE to dictionary add FID from relationship table
with arcpy.da.SearchCursor(fc3,['GlobalID','LRType']) as cursor:
    for row in cursor:
        LAP.append(row)

del cursor


with arcpy.da.SearchCursor(fc2,['GlobalID','LRType']) as cursor:
    for row in cursor:
        LAA.append(row)

del cursor


with arcpy.da.SearchCursor(fc1,['GlobalID','LAPsGlobalID','LAAGlobalID']) as cursor:
    for row in cursor:
        Relates.append(row)

del cursor

print Relates[1]



#Search Cursor through LAP saving global ID and LRTYPE to dictionary add FID from relationship table

#combine the two above based on FID

#LOOP over dictionary finding where LRTYPES DONT MATCH STORE fid in list

#LOOP over relationship table and delete if FID matches



