#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     23/04/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

#The GDB which the feature whos geometry will change lives
workspace = arcpy.GetParameterAsText(0)
#The feature who geometry will change
fc1 = arcpy.GetParameterAsText(1)
#The feature with the geometry to be appeneded in
fc2 = arcpy.GetParameterAsText(2)
#The uniqueField to base the join on
uniqueFieldInput = arcpy.GetParameterAsText(3)
uniqueFieldCorrected = arcpy.GetParameterAsText(4)



#Start Edditing
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

count = 0

#Append in old geometry for features
ownershipFields = [uniqueFieldCorrected,'SHAPE@']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc2,ownershipFields)}
print "Updating Geometry"
updateFields = [uniqueFieldInput,'SHAPE@']
with arcpy.da.UpdateCursor(fc1, updateFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:

            if updateRow[1]!= valueDict[keyValue][0]:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
                count = count + 1
                updateRow[1] = valueDict[keyValue][0]
                updateRows.updateRow(updateRow)


edit.stopOperation()
edit.stopEditing(True)

arcpy.AddMessage((str(count) +" Features Updated"))