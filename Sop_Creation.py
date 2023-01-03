#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     31/01/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

working = workingGBD

fc1 = LOP
fc2 = HMLR
fc3 = Relates
fc4 = SafegaurdingOld
fc5 = SafegaurdingNew
fc6 = LOP_SafegaurdingNew
fc7 = LOP_SafegaurdingNew_Dissolved
fc8 = LOP_SafegaurdingOld
fc9 = LOP_SafegaurdingOldDissolve
fc11 = LOP_In_Safegarding_Limits_Registered
fc12 = LOP_In_Safegarding_Limits_Unregistered
fc13 = LOP_In_Safegarding_Limits_Registered_HMLR
fc14 = LOP_In_Safegarding_Limits_Unregistered_HMLR



LOPGlobalID = "LOPGlobalID"
HMLRGlobalID = "HMLRGlobalID"

LOPGlobalIDFields = ['GlobalID', LOPGlobalID ]
HMLRGlobalIDFields = ['GlobalID', HMLRGlobalID]

LOP_SafegaurdingNewDissovleFields = ['LOPGlobalID','Zone_Type','OwnershipReferenceNumber']
LOP_SafegaurdingNewDissovleAddFields = ['Include']
LOP_SafegaurdingNewUpdateFields = ['OwnershipReferenceNumber','LOPGlobalID']
LOP_UpdateFields = ['OwnershipReferenceNumber','LOPGlobalID']

updateRow
#AddFields to write the global ID'S to a string
arcpy.AddField_management(fc1,LOPGlobalID,'STRING')
arcpy.AddField_management(fc2,HMLRGlobalID,'STRING')

#Loop Through LOP and write Gloabl ID to a new Field
with arcpy.da.UpdateCursor(fc1, LOPGlobalIDFields) as updateRow:
    for row in updateRow:
        row[1] = row[0]

del updateRow

#loop through HML and write Global ID too a new fields
with arcpy.da.UpdateCursor(fc2, HMLRGlobalIDFields) as updateRow:
    for row in updateRow:
        row[1] = row[0]

del updateRow

#Intersect LOP with Newsafegaurding and Dissolve to only keep Ownership Reference Number, Global ID and Zone Type
arcpy.Intersect_analysis([fc1,fc5],fc6, "ALL", "", "INPUT")
arcpy.Dissolve_management(fc6,fc7,LOP_SafegaurdingNewDissovleFields)
#Add a field to hold if a parcel is in new safegaurding
arcpy.AddField_management(fc1,LOP_SafegaurdingNewDissovleAddFields,'STRING')

#Create a dictionary for parcels in New Safeguarding, loop through and populate the field in original land ownerhsip layer
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc7,LOP_SafegaurdingNewUpdateFields)}

with arcpy.da.UpdateCursor(fc1, LOP_UpdateFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = "Yes"
            updateRows.updateRow(updateRow)
del valueDict, updateRows


#Intersect LOP with Old safegaurding and Dissolve to only keep Ownership Reference Number, Global ID and Zone Type
arcpy.Intersect_analysis([fc1,fc4],fc6, "ALL", "", "INPUT")
arcpy.Dissolve_management(fc8,fc9,LOP_SafegaurdingNewDissovleFields)

#Create a dictionary for parcels in old Safeguarding, loop through and populate the field in original land ownerhsip layer
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc9,LOP_SafegaurdingNewUpdateFields)}

with arcpy.da.UpdateCursor(fc1, LOP_UpdateFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            if updateRow[1] == "Yes":
                pass
            else:

                updateRow[1] = "Yes"
                updateRows.updateRow(updateRow)

del valueDict, updateRows

#Select Out Ownership Parcles that fall within either dafegaurding limits and split by registered vs unregistered.
arcpy.Select_analysis(fc1, fc11, "[Include] = 'Yes' AND [ExternalReference] IS NULL")
arcpy.Select_analysis(fc1, fc12, "[Include] = 'Yes' AND [ExternalReference] IS NOT NULL")

arcpy.Intersect_analysis([fc2,fc11],fc6, "ALL", "", "INPUT")
arcpy.Dissolve_management(fc2,fc12,LOP_SafegaurdingNewDissovleFields)




