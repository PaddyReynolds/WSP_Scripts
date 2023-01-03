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

workspace = r'C:\Users\UKPXR011\Desktop\Safeguarding\Leeds_HMLR\L3L4_SG_21042020_PR_1\L3L4_SG_21042020_PR_1\AmendsFolder_202004210851\L3L4_SG_21042020_PR_1_1.gdb'
scratch = r'C:\Users\UKPXR011\Desktop\Safeguarding\Leeds_HMLR\Scratch.gdb'
fc1 = r'C:\Users\UKPXR011\Desktop\Safeguarding\Leeds_HMLR\L3L4_SG_21042020_PR_1\L3L4_SG_21042020_PR_1\AmendsFolder_202004210851\L3L4_SG_21042020_PR_1_1.gdb\STATUTORY_PROCESSES\HMLR_Parcels'
fc2 = r'C:\Users\UKPXR011\Desktop\Safeguarding\Leeds_HMLR\L3L4_SG_21042020_PR_1\L3L4_SG_21042020_PR_1\AmendsFolder_202004210851\L3L4_SG_21042020_PR_1_1.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'
fc3 = scratch + '\\HMLR_LOP'
fc4 = scratch + '\\HMLR_LOP_Dissolve'
HMLR_Unique_Fields = ['GlobalID','HMLR_Unique_ID']
'''
#Add a Field
arcpy.AddField_management(fc1, 'HMLR_Unique_ID', "TEXT","","","", "", "", "", "")

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

cursor = arcpy.da.UpdateCursor(fc1,HMLR_Unique_Fields)
for row in cursor:
    row[1]=str(row[0])
    cursor.updateRow(row)
del cursor

edit.stopOperation()
edit.stopEditing(True)


arcpy.Intersect_analysis([fc1,fc2],fc3)
arcpy.Dissolve_management(fc3, fc4,'HMLR_Unique_ID')
ownershipFields = ['HMLR_Unique_ID','SHAPE@']
with arcpy.da.UpdateCursor(fc4, ownershipFields) as updateRows:
    for updateRow in updateRows:
        if updateRow[1] <2:
            updateRows.deleteRow()

valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc4,ownershipFields)}

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

with arcpy.da.UpdateCursor(fc1, ownershipFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRows.deleteRow()

edit.stopOperation()
edit.stopEditing(True)