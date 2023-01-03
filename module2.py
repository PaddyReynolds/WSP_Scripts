#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      UKPXR011
#
# Created:     12/12/2019
# Copyright:   (c) UKPXR011 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from time import strftime

print "Start script: " + strftime("%Y-%m-%d %H:%M:%S")

import arcpy

workspace =r'C:\Users\UKPXR011\Desktop\Paddy_Work\Mailing_List\CP2_1_List\CP2_1_Sift.gdb'
sourceFC = r'C:\Users\UKPXR011\Desktop\Paddy_Work\Mailing_List\CP2_1_List\CP2_1_Sift.gdb\STATUTORY_PROCESSES\AccessLicences'

sourceFieldsList =['GlobalID','LicenceID']
# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(sourceFC, sourceFieldsList)}

updateFC = r'C:\Users\UKPXR011\Desktop\Paddy_Work\Mailing_List\CP2_1_List\CP2_1_Sift.gdb\STATUTORY_PROCESSES\relAccessLicences_LandOwnership'

updateFieldsList = ['AccessLicenceGlobalID','I_Am_An_Idiot']


edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()


with arcpy.da.UpdateCursor(updateFC, updateFieldsList) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

del valueDict

edit.stopOperation()
edit.stopEditing(True)

print "Finished script: " + strftime("%Y-%m-%d %H:%M:%S")