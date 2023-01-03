#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     17/02/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

env = r'C:\Users\UKPXR011\Desktop\Super Tracker\GIS\OwnershipSchema\GDD\2C866-WSP-GI-GDD-100-000003_P142\YW8.gdb'

edit = arcpy.da.Editor(env)
edit.startEditing(False, True)
edit.startOperation()

fc1 = r'C:\Users\UKPXR011\Desktop\Super Tracker\GIS\OwnershipSchema\GDD\2C866-WSP-GI-GDD-100-000003_P142\YW8.gdb\topo\PRP_WSP_2C866_LD_LandAccess_Ply'
fc2 = r'C:\Users\UKPXR011\Desktop\Super Tracker\GIS\OwnershipSchema\GDD\Extract.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'
fc3 = r'C:\Users\UKPXR011\Desktop\Super Tracker\GIS\OwnershipSchema\GDD\Extract.gdb\STATUTORY_PROCESSES\HMLR_Parcels'
fc4 = r'C:\Users\UKPXR011\Desktop\Super Tracker\GIS\OwnershipSchema\GDD\Extract.gdb\STATUTORY_PROCESSES\AccessLicences'
fc5 = r'C:\Users\UKPXR011\Desktop\Super Tracker\GIS\OwnershipSchema\GDD\Extract.gdb\AL_LOP'
fc6 = r'C:\Users\UKPXR011\Desktop\Super Tracker\GIS\OwnershipSchema\GDD\Extract.gdb\LOP_HMLR'

FieldList = ['L_Relate','OwnershipNumber','OwnershipRelate','HMLR_Relate']

fields = arcpy.ListFields(fc1)

for field in FieldList:
    if field in fields:
        print str(field) +" Already Exists"
        pass
    else:
        arcpy.AddField_management(fc1,field, "TEXT","","","", "", "", "", "")

'''
arcpy.AddField_management(fc1, 'L_Relate', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc1, 'OwnershipNumber', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc1, 'OwnershipRelate', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc1, 'HMLR_Relate', "TEXT","","","", "", "", "", "")
'''


FieldsJoin = ['LicenceID','GlobalID']
FieldsUpdate = ['LicenceNum','L_Relate']

# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc4,FieldsJoin)}

with arcpy.da.UpdateCursor(fc1,FieldsUpdate) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = str(valueDict[keyValue][0])
            updateRows.updateRow(updateRow)

del valueDict


#Get_LOP_RelationshipGlobalID From Table
FieldsJoin = ['AccessLicenceGlobalID','LOwnGlobalID',]
FieldsUpdate = ['L_Relate','OwnershipRelate']

# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc5,FieldsJoin)}

with arcpy.da.UpdateCursor(fc1, FieldsUpdate) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = str(valueDict[keyValue][0])
            updateRows.updateRow(updateRow)

del valueDict


#Get_LOP_RelationshipGlobalID From Table
FieldsJoin = ['GlobalID','OwnershipReferenceNumber']
FieldsUpdate = ['OwnershipRelate','OwnershipNumber']

# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc2,FieldsJoin)}

with arcpy.da.UpdateCursor(fc1, FieldsUpdate) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = str(valueDict[keyValue][0])
            updateRows.updateRow(updateRow)

del valueDict


#Get_LOP_RelationshipGlobalID From Table
FieldsJoin = ['LOwnGlobalID','HmlrGlobalID']
FieldsUpdate = ['OwnershipRelate','HMLR_Relate']

# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc6,FieldsJoin)}

with arcpy.da.UpdateCursor(fc1, FieldsUpdate) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = str(valueDict[keyValue][0])
            updateRows.updateRow(updateRow)

del valueDict


#Get_LOP_RelationshipGlobalID From Table
FieldsJoin = ['GlobalID','HMLR_Title_No']
FieldsUpdate = ['HMLR_Relate','TitleNum']

# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc3,FieldsJoin)}

with arcpy.da.UpdateCursor(fc1, FieldsUpdate) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = str(valueDict[keyValue][0])
            updateRows.updateRow(updateRow)

del valueDict

edit.stopOperation()
edit.stopEditing(True)

print "done"
