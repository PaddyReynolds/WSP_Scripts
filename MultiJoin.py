#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     10/12/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from time import strftime

print( "Start script: " + strftime("%Y-%m-%d %H:%M:%S"))

import arcpy

sourceFC = r"C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Extract\23122021.gdb\Fixes"

desc= arcpy.Describe(sourceFC)

gdb = desc.path

print gdb



sourceFieldsList = ["LAPID", "LAAID", "LAPStatus"]

# Use list comprehension to build a dictionary from a da SearchCursor where the key values are based on 3 separate feilds
valueDict = {str(r[0]) + "," + str(r[1]):(r[2:]) for r in arcpy.da.SearchCursor(sourceFC, sourceFieldsList)}

updateFC = r"C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Extract\10022022.gdb\LAP"


gdb = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Extract\10022022.gdb'

#edit = arcpy.da.Editor(gdb)
#edit.startEditing(False, True)
#edit.startOperation()

updateFieldsList = ["LAPID", "LAAID", "LAPStatus"]

with arcpy.da.UpdateCursor(updateFC, updateFieldsList) as updateRows:
    for updateRow in updateRows:
        # store the Join value by combining 3 field values of the row being updated in a keyValue variable
        keyValue = updateRow[0]+ "," + str(updateRow[1])
        # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[2] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

del valueDict

#edit.stopOperation()
#edit.stopEditing(True)
print( "Finished script: " + strftime("%Y-%m-%d %H:%M:%S"))
