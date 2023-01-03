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
workspace = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Leeds\NPS_Update.gdb'
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Leeds\NPS_Update.gdb\STATUTORY_PROCESSES\HMLR_Parcels'
fc2 = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Leeds\Output.gdb\Changed'


#Start Edditing
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()
#                 0             1               2                       3          4            5           6           7           8           9       10          11          12          13         14       15              16
hs2_Fields =['HS2_AssetID','HS2_AssetName','HS2_SuitabilityCode','HS2_Phase','HS2_DocNum','HS2_DocRev','Contract','Originator','HS2_SupDoc','LAPID', 'LAPStatus', 'LAPDesc', 'NumOnPlan', 'LAAID', 'LAAName', 'LRType', 'NoticeType']
#Append in old geometry for features
ownershipFields = ['POLY_ID','SHAPE@']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc2,ownershipFields)}
print "Updating Geometry"
updateFields = ['uid','SHAPE@']
with arcpy.da.UpdateCursor(fc1, updateFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)


edit.stopOperation()
edit.stopEditing(True)
