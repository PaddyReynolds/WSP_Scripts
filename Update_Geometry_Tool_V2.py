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
workspace = r'C:\Users\UKPXR011\Desktop\Current Work\2b\AP2\Schedule_And_Plans\CCB_Update.gdb'
#The feature who geometry will change
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\2b\AP2\Schedule_And_Plans\CCB_Update.gdb\STATUTORY_PROCESSES\Limits'
#The feature with the geometry to be appeneded in
fc2 = r'C:\Users\UKPXR011\Documents\ArcGIS\Default.gdb\HS2_MWJ_2PT24_LD_Consolidate4'
#The uniqueField to base the join on
uniqueFieldInput = 'LimitDescription'
uniqueFieldCorrected = 'Reference'

fc3 = workspace + "\Edited_Parcels"

#arcpy.CreateFeatureclass_management (workspace, "Edited_Parcels","POLYGON", fc1,"SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE",fc1)
#arcpy.AddField_management(fc3,"UIQUE_REF","TEXT","","",1000, "", "", "", "")

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
insert_Fields = ['UIQUE_REF','SHAPE@']
#with arcpy.da.InsertCursor(fc3,insert_Fields) as insertrows:
with arcpy.da.UpdateCursor(fc1, updateFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:

            if updateRow[0]!= valueDict[keyValue][0]:
                #insertrows.insertRow(updateRow)
             # transfer the value stored under the keyValue from the dictionary to the updated field.
                count = count + 1
                updateRow[1] = valueDict[keyValue][0]
                updateRows.updateRow(updateRow)


edit.stopOperation()
edit.stopEditing(True)

arcpy.AddMessage((str(count) +" Features Updated"))