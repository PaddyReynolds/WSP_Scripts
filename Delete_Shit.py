#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     17/04/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy

workspace =r'C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\Relates_Update\ABP_Relates.gdb'
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\Relates_Update\ABP_Relates.gdb\STATUTORY_PROCESSES\ABP_Polygon'

shitRows= 0

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

with arcpy.da.UpdateCursor(fc1, 'ObjectID') as updateRows:
    for updateRow in updateRows:

        shitRows = shitRows + 1
        updateRows.deleteRow()


edit.stopOperation()
edit.stopEditing(True)
print shitRows
print "Done"