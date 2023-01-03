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
fc2 = r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS\Scratch.gdb\CP3_SG_OLD_1'
fc3 = out_path+'\NPS_CP3_SG_Temp'
fc4 = out_path+'\NPS_CP3_SG_Temp_Dissolved'
fc5 = out_path+'\HMLR_CP3SG'
fc6 = r'C:\Users\UKPXR011\Desktop\Safeguarding\PR_Model\PR_Model\SOP_Final.gdb\STATUTORY_PROCESSES\HMLR_Parcels'
fc7 = out_path+'\HMLR_CP3SG_Final'

dissolvefields ='TITLE_NO'

print 'intersect started'
intersectNPS = arcpy.Intersect_analysis([fc1,fc2], fc3, "ALL", "", "INPUT")
print 'intersect done'
print 'Dissolve Started'
intersectNPSDissolve = arcpy.Dissolve_management(fc3,fc4,dissolvefields)
print 'Dissolve Done'

arcpy.AddField_management(fc1, 'CP3_SG_OLD', "STRING","","","", "", "", "", "")

UpdateFields = ['TITLE_NO','CP3_SG_OLD']
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
arcpy.Select_analysis(fc1, fc5, "CP3_SG_OLD = 'Yes'")
arcpy.Dissolve_management(fc5,fc7,dissolvefields)
arcpy.AddField_management(fc7, 'Held', "STRING","","","", "", "", "", "")
print 'Exported NPS'

UpdateFields = ['TITLE_NO','Held']
print 'Removing HMLR already heald'
valueDict1 = {r[0] for r in arcpy.da.SearchCursor(fc6,['HMLR_Title_No'])}
with arcpy.da.UpdateCursor(fc7, UpdateFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict1:
            updateRow[1] = 'Yes'
            updateRows.updateRow(updateRow)

print 'Done'
print 'Dissolving to get unique Title Numers'
acreRows =['SHAPE_Area', 'Acre']
arcpy.AddField_management(fc7, 'Acre', "STRING","","","", "", "", "", "")

print 'Finding Titles greater than one acre'
with arcpy.da.UpdateCursor(fc7, acreRows) as updateRows:
    for updateRow in updateRows:

        if updateRow[0]>=4046.86:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
             updateRow[1] = 'Yes'
             updateRows.updateRow(updateRow)



