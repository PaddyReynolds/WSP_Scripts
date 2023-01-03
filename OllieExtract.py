#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     21/02/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
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
from collections import Counter

arcpy.env.overwriteOutput = True

gdb = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Scratch.gdb'
finished = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\SLOPS.gdb'
workspace=r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Extract.gdb'

fc1= r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Extract.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'

fc2= r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Extract.gdb\STATUTORY_PROCESSES\HMLR_Parcels'

fc3 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Extract.gdb\STATUTORY_PROCESSES\relLandOwnership_HMLR'

fc4 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Scratch.gdb\\SLOP_Input_LOP'

fc5 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Scratch.gdb\SLOP_Input_LOP_Temp'

fc6 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Scratch.gdb\New_Safeguarding'

fc7= r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Scratch.gdb\Old_Safeguarding'

fc8 = gdb+"\SG_New_Intersect"

fc9 = gdb+"\SG_New_Intersect_Dissolve"

fc10 =gdb+"\SG_Old_Intersect"

fc11 = gdb+"\SG_Old_Intersect_Dissolve"

fc12 = gdb+"\DissolvedHMLR"

fc13 = gdb+"\SLOP_Input_Hmlr_Intersect"

fc14 = gdb+"\SLOP_Input_Hmlr_Intersect_Dissolve"

fc15 = finished+"\Safeguarding_Land_Ownership_Parcels"

fc16 = gdb+"\Unumbers"

print "Adding Required Fields"
#Add the fields to hold the globalID
arcpy.AddField_management(fc1, 'LOP_Unique_ID', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc2, 'HMLR_Unique_ID', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc1, 'Include', "TEXT","","","", "", "", "", "")
LOP_Unique_Fields = ['GlobalID','LOP_Unique_ID']
HMLR_Unique_Fields = ['GlobalID','HMLR_Unique_ID']

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

print"Updating Unique Field for LOP and HMLR"
#Update the fields holding the global ID with a cursor
cursor = arcpy.da.UpdateCursor(fc1,LOP_Unique_Fields)
for row in cursor:
    row[1]=str(row[0])
    cursor.updateRow(row)

del cursor

cursor = arcpy.da.UpdateCursor(fc2,HMLR_Unique_Fields)
for row in cursor:
    row[1]=str(row[0])
    cursor.updateRow(row)
del cursor


print "Updating New Safegaurding and LOP"
#Intersect and Dissolve the New Safegaurding Area
arcpy.Intersect_analysis([fc1,fc6],fc8)
arcpy.Dissolve_management(fc8, fc9,'LOP_Unique_ID')

print "Updating Old Safegaurding and LOP"
#Intersect and Dissolve the Old Safegaurding Area
arcpy.Intersect_analysis([fc1,fc7],fc10)
arcpy.Dissolve_management(fc10, fc11,'LOP_Unique_ID')


JoinFields = ['LOP_Unique_ID','OBJECTID']
Update_Fields = ['LOP_Unique_ID','Include']
# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc9,JoinFields)}
valueDict1 = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc11,JoinFields)}
print "Updating Parcels required for safegaurding"
#Update the Inlcude field to show which LOPs were intersected by old and new safeguarding
with arcpy.da.UpdateCursor(fc1, Update_Fields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = 'Yes'
            updateRows.updateRow(updateRow)

        if keyValue in valueDict1:

            # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = 'Yes'
            updateRows.updateRow(updateRow)

edit.stopOperation()
edit.stopEditing(True)

#Select only parcels that are needed for safegaurding
print "Extract LOP's for safeguaridng"
arcpy.Select_analysis(fc1, fc4,"""Include = 'Yes'""")