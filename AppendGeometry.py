#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     19/02/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy

fc1=r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\Scratch.gdb\SLOP_Input_LOP'
fc2=r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\Scratch.gdb\Insercet_Dissolve_Test_OB'

ownershipFields = ['LOP_Unique_ID','SHAPE@']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc1,ownershipFields)}

with arcpy.da.UpdateCursor(fc2, ownershipFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)