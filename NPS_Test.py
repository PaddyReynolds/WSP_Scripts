#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     23/01/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

arcpy.env.overwriteOutput = True
arcpy.env.workspace = r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS\Scratch.gdb'

# Set local variables
out_path = r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS\Scratch.gdb'
fc1 = r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS\National_Polygon_Service_January2020_FullSupply\National_Polygon_Service_January2020_FullSupply_1.gdb\GEODATA\L3L4_NPS'
fc2 = r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS\Scratch.gdb\Safeguarding_Limit'
fc3 = out_path+'\NPS_SafeguardingLimit_Temp'
fc4 = out_path+'\NPS_SafeguardingLimit_Temp_Dissolved'
fc5 = out_path+'\HMLR_SafeguardingLimit'
fc6 = r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS\Scratch.gdb\HMLR_Parcels_1'
fc7 = out_path+'\HMLR_SafeguardingLimit_Final'

dissolvefields ='TITLE_NO'

print 'intersect started'
intersectNPS = arcpy.Intersect_analysis([fc1,fc2], fc3, "ALL", "", "INPUT")
print 'intersect done'
print 'Dissolve Started'
intersectNPSDissolve = arcpy.Dissolve_management(fc3,fc4,dissolvefields)
print 'Dissolve Done'

arcpy.AddField_management(fc1, 'SafeGaurding_Limit', "STRING","","","", "", "", "", "")

UpdateFields = ['TITLE_NO','SafeGaurding_Limit']
# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0] for r in arcpy.da.SearchCursor(fc4,dissolvefields)}

print 'Search Cursor started'
with arcpy.da.UpdateCursor(fc1, UpdateFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = "Yes"
            updateRows.updateRow(updateRow)
del updateRows

print 'Search Cursor Done'

print 'Exporting Intersecting NPS'
arcpy.Select_analysis(fc1, fc5, "SafeGaurding_Limit = 'Yes'")
print 'Exported NPS'

print 'Removing HMLR already heald'
valueDict1 = {r[0] for r in arcpy.da.SearchCursor(fc6,['HMLR_Title_No'])}
with arcpy.da.UpdateCursor(fc5, UpdateFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             updateRows.deleteRow()

print 'Done'
fc7 = out_path+'\HMLR_SafeguardingLimit_Final'
print 'Dissolving to get unique Title Numers'
arcpy.Dissolve_management(fc5,fc7,dissolvefields)

acreRows =['SHAPE_Area', 'Acre']
arcpy.AddField_management(fc5, 'Acre', "STRING","","","", "", "", "", "")

print 'Finding Titles greater than one acre'
with arcpy.da.UpdateCursor(fc5, UpdateFields) as updateRows:
    for updateRow in updateRows:

        if updateRow[0]>=4046.86:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
             updateRow[1] = 'Yes'
             updateRows.updateRow(updateRow)



