#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     11/06/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

def findField(fc, fi):
  fieldnames = [field.name for field in arcpy.ListFields(fc)]
  if fi in fieldnames:
    return True
  else:
    return False

workspace = r'C:\Users\UKPXR011\Desktop\Scripts\L3_L4_Split\Scratch.gdb'
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Leeds\Extract.gdb\Slops'
fc2 = r'C:\Users\UKPXR011\Desktop\Scripts\L3_L4_Split\Scratch.gdb\L3L4MML'
fc3 = workspace + '\Intersect_LOP'
fc4 = workspace + '\Limit_Lop'
DissolveFields =['Ownership_Reference_Numbers', 'LimitDescription']
arcpy.env.overwriteOutput = True
Field_Name = 'L3L4MML'
updateFields = ['Ownership_Reference_Numbers', 'L3L4MML']

fieldTest=findField(fc1,Field_Name)

if findField(fc1,Field_Name) == False:
    arcpy.AddField_management(fc1,Field_Name,"Text")

else:
    print 'Field already exists'
    pass

#Intersect and Dissolve to get a list of OwnershipReferenceNumbers vs Limits.
arcpy.Intersect_analysis([fc1,fc2],fc3)
arcpy.Dissolve_management(fc3, fc4,DissolveFields)


#Append in old geometry for features
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc4,DissolveFields)}
with arcpy.da.UpdateCursor(fc1, updateFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]

        if keyValue in valueDict:
            updateRow[1]= valueDict[keyValue][0]
            updateRows.updateRow(updateRow)
         # verify that the keyValue

        else:
            updateRow[1]= 'Parcel Not In Limits'
            updateRows.updateRow(updateRow)





