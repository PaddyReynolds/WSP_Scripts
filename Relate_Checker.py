#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     28/05/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

extract =
scratch =

f1 = relationship table
f2 =lops
fc3 = limits
fc4 = scratch  + 'Limit'
fc6 = scratch + 'LOP_Intersect_'
fc7 = scratch  + 'Limit'
fc8 = scratch + 'Limit_Lops'
fc9 = scratch + 'Relationships'
fc10 = scratch  + 'Limit'


arcpy.AddField_management(fc2, 'LOP_Unique_ID', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc2, 'Intersect_Limit', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc2, 'Related_Limit', "TEXT","","","", "", "", "", "")

arcpy.Select_analysis(fc3, fc4,"""LimitDescription = 'Consolidated Construction Boundary CP01'""")
#Intersect Dissolve
Dissolve_Fields = ['OwnershipReferenceNumber']
arcpy.Intersect_analysis([fc4,fc2],fc6)
arcpy.Dissolve_management(fc6, fc8,Dissolve_Fields)

edit = arcpy.da.Editor(extract)
edit.startEditing(False, True)
edit.startOperation()

JoinFields = ['OwnershipReferenceNumber','OBJECTID']
Update_Fields = ['OwnershipReferenceNumber','Intersect_Limit']
# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc8,JoinFields)}
print "Updating Parcels required for safegaurding"
#Update the Inlcude field to show which LOPs were intersected by old and new safeguarding
with arcpy.da.UpdateCursor(fc2, Update_Fields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = 'Yes'
            updateRows.updateRow(updateRow)


LOP_Unique_Fields = ['GlobalID','LOP_Unique_ID']
cursor = arcpy.da.UpdateCursor(fc2,LOP_Unique_Fields)
for row in cursor:
        row[1]=str(row[0])
        cursor.updateRow(row)
del cursor

edit.stopOperation()
edit.stopEditing(True)



arcpy.Select_analysis(fc1, fc9)






