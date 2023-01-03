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
workspace = r'C:\Users\UKPXR011\Desktop\Scripts\Update_Geometry\Scratch.gdb'
#The feature who geometry will change
fc1 = r'C:\Users\UKPXR011\Desktop\Scripts\Update_Geometry\Scratch.gdb\Feature1'
#The feature with the geometry to be appeneded in
fc2 = r'C:\Users\UKPXR011\Desktop\Scripts\Update_Geometry\Scratch.gdb\Feature_2'
#The uniqueField to base the join on
uniqueField = "UID"
uniqueFieldCorrected = 'UID'
fc3 = workspace + "\Edited_Parcels"

updateFields = [f.name for f in arcpy.ListFields(fc1)]
updateFields.append('SHAPE@')
UIDRow = updateFields.index(uniqueField)
print updateFields
ShapeRow = updateFields.index('SHAPE@')
print ShapeRow

arcpy.CreateFeatureclass_management (workspace, "Edited_Parcels","POLYGON", fc1,"SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE",fc1)


#Start Edditing
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

count = 0
#Append in old geometry for features
ownershipFields = [uniqueField,'SHAPE@']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc2,ownershipFields)}
print "Updating Geometry"
#updateFields = ['uid','SHAPE@']
with arcpy.da.InsertCursor(fc3,updateFields) as insertrows:
    with arcpy.da.UpdateCursor(fc1, updateFields) as updateRows:
        for updateRow in updateRows:
            # store the Join value of the row being updated in a keyValue variable
            keyValue = updateRow[UIDRow]
             # verify that the keyValue is in the Dictionary
            if keyValue in valueDict:

                if updateRow[UIDRow]!= valueDict[keyValue][0]:
                    insertrows.insertRow(updateRow)
                 # transfer the value stored under the keyValue from the dictionary to the updated field.
                    count = count + 1
                    updateRow[ShapeRow] = valueDict[keyValue][0]
                    updateRows.updateRow(updateRow)


edit.stopOperation()
edit.stopEditing(True)

arcpy.AddMessage((str(count) +" Features Updated"))