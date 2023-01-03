#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     12/12/2022
# Copyright:   (c) UKPXR011 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from time import strftime
import arcpy

print( "Start script: " + strftime("%Y-%m-%d %H:%M:%S"))

sourceFC = r"C:\Users\UKPXR011\Desktop\Current Work\2b\AP2\Plot_Sync\CDES_Plot_Updates_06122022.gdb\STATUTORY_PROCESSES\Plots"

sourceFieldsList = ["BoundaryCodeID", "LandReferenceNo", "UniqueID"]

# Use list comprehension to build a dictionary from a da SearchCursor where the key values are based on 3 separate feilds
valueDict = {str(r[0]) + "," + str(r[1]):(r[2:]) for r in arcpy.da.SearchCursor(sourceFC, sourceFieldsList)}

updateFC = r"C:\Users\UKPXR011\Desktop\Current Work\2b\AP2\Plot_Sync\Plot_Updates_12122022\Scratch.gdb\Plot_Updates"

updateFieldsList = ["Boundary_Code", "Plot_Number", "Unique_Plot_ID"]

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

print( "Finished script: " + strftime("%Y-%m-%d %H:%M:%S"))