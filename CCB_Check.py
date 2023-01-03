#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     18/06/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os

workspace = r'C:\Users\UKPXR011\Desktop\QC Work\Manchester CCB_Check\Topo_Check.gdb'
fc1 = r'C:\Users\UKPXR011\Desktop\QC Work\Manchester CCB_Check\Topo_Check.gdb\Topo\P04'
fc2 = r'C:\Users\UKPXR011\Desktop\QC Work\Manchester CCB_Check\Topo_Check.gdb\Topo\P05'
n = 9
n1=8


# Get a list of fields from the InputLOP feature
UpdateFields = [f.name for f in arcpy.ListFields(fc1)]
#Delete the first 9 from the list as they dont need updating
#print UpdateFields

#Get a list of fields from SDE
CurrentFields = [f.name for f in arcpy.ListFields(fc2)]
#Delete the first 8 as they dont need to be updated

valueDict = {r[31]:(r[1:]) for r in arcpy.da.SearchCursor(fc1,UpdateFields)}
'''
with arcpy.da.SearchCursor(fc2, CurrentFields) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[]
'''



