#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     26/03/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import shutil

fc1 = 'NPS'
fc2 = r'C:\Users\UKPXR011\Desktop\Scripts\NPS_Automation\Scratch.gdb\HMLR_Schema'

field = ['OBJECTID']

with arcpy.da.UpdateCursor(fc2,field) as cursor:
    for row in cursor:
        cursor.deleteRow()

del cursor

print 'Deleted Them Cunts'