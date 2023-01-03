#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     13/01/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

fc1 =r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Scratch.gdb\Test_Intersect'
scratch = r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Scratch.gdb'
duplicateField = 'Ownership Reference Number'
dupField = list(duplicateField)
dissolveStats = str(duplicateField + 'MAX')
DissolveTemp = str(scratch +'\TempDissolve')
fc2 = arcpy.Dissolve_management(fc1,DissolveTemp,dupField,dissolveStats)
DictFields =list(duplicateField,'MAX_SHAPE_Area')
UpdateFeilds = list(duplicateField, 'Shape_Area')

valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc4,DictFields)}
#Delete the rows where the shape area doesnt match the max area (are not the largest duplicate)
with arcpy.da.UpdateCursor(fc3,UpdateFeilds) as updateRows:

    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in valueDict:
            if updateRow[1] < valueDict[keyValue][0]:
                updateRows.deleteRow()
                #updateRows.updateRow(updateRow)


Acpy.addmessage("Complete")