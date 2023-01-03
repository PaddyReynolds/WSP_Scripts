#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     08/06/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os

workspace = 'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\LeedsSLOPS_Final\Mailing_List_Slops_05062020_1.gdb'
desktopPath = 'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\LeedsSLOPS_Final\Output'
fc1 = 'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\LeedsSLOPS_Final\Output\Output.gdb\Required_LOP'
fc2 = 'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\LeedsSLOPS_Final\Mailing_List_Slops_05062020_1.gdb\STATUTORY_PROCESSES\Safeguarding_Land_Ownership_Parcels'
n = 9
n1=8


UpdateFields = [f.name for f in arcpy.ListFields(fc1)]
del UpdateFields[:n]
UpdateFields.insert(0,"OwnershipReferenceNumber")
#print UpdateFields


CurrentFields = [f.name for f in arcpy.ListFields(fc2)]
del CurrentFields[:n1]
CurrentFields.insert(0,"OwnershipReferenceNumber")
print CurrentFields
#print CurrentFields



#Append in old geometry for features
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc1,UpdateFields)}
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()
with arcpy.da.UpdateCursor(fc2, CurrentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:

                for i in range(1,70):
                    n = i-1
                    #print i
                    # transfer the value stored under the keyValue from the dictionary to the updated field.
                    updateRow[i] = valueDict[keyValue][n]
                    updateRows.updateRow(updateRow)

                updateRow[71] = valueDict[keyValue][72]
                updateRow[72] = valueDict[keyValue][73]
                updateRow[73] = valueDict[keyValue][74]
                updateRow[74] = valueDict[keyValue][75]
                updateRow[75] = valueDict[keyValue][76]
                updateRow[76] = valueDict[keyValue][77]
                updateRow[77] = valueDict[keyValue][71]



edit.stopOperation()
edit.stopEditing(True)
