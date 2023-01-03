# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     03/07/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os

arcpy.env.overwriteOutput = True

cunt = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Leeds\Scratch.gdb'
workspace = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Leeds\National_Polygon_Service_July2020_FullSupply.gdb'

fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Leeds\National_Polygon_Service_July2020_FullSupply.gdb\NPS_L3L4'
fc2 = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Leeds\Scratch.gdb\New_Safeguarding'
fc3 = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Leeds\Scratch.gdb\Old_Safeguarding'
fc4 = cunt + "\\"+ "merged_safegaurding"
fc5 = cunt + "\\"+ "merged_Dissolved_sg"
fc6 = cunt + "\\"+ "merged_sg_intersect"
fc7 = cunt + "\\"+ "merged_sg_intersect_dissovle"
fc8 = cunt + "\\"+"required_NPS"
fc9 = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Leeds\Scratch.gdb\HMLR'
fc10 = cunt + "\\"+"HMLR_Intersect_Temp"
fc11 = cunt + "\\"+"HMLR_Intersect_Temp_Dissolve"
fc12 = cunt + "\\"+"HMLR_SG"
fc13 = cunt +"\\" + "HMLR_SG_Dissolved"
fc14 = cunt + "\\"+ "NPS_Dissolved"

'''
arcpy.Merge_management ([fc2, fc3],fc4)
arcpy.Dissolve_management(fc4,fc5)
print 'Combined SG'

print 'Intersecting'
arcpy.Intersect_analysis([fc1,fc5],fc6)
dissolveFields = ['TITLE_NO']
arcpy.Dissolve_management(fc6,fc7,dissolveFields)


arcpy.AddField_management(fc1,"Include","TEXT","","",50, "", "", "", "")

print 'Updating NPS'
UpdateFields = ['TITLE_NO','OBJECTID']
#Make A dictionary out of the required LOP plus update fields
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc7,UpdateFields)}

currentFields = ['TITLE_NO','Include']
#Start Edditing
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc1, currentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRow[1] == 'Yes'
            updateRows.updateRow(updateRow)

edit.stopOperation()
edit.stopEditing(True)

arcpy.Select_analysis(fc1, fc8,"""Include = 'Yes'""")
print 'extracting NPS'
'''
arcpy.Intersect_analysis([fc9,fc5],fc10)
dissolveFields = ['HMLR_Title_No']
arcpy.Dissolve_management(fc10,fc11,dissolveFields)

print 'Fannying on with HMLR'
arcpy.AddField_management(fc9,"Include","TEXT","","",50, "", "", "", "")

UpdateFields = ['HMLR_Title_No','OBJECTID']
#Make A dictionary out of the required LOP plus update fields
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc11,UpdateFields)}

currentFields = ['HMLR_Title_No','Include']

#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc9, currentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRow[1] == 'Yes'
            updateRows.updateRow(updateRow)

arcpy.Select_analysis(fc9, fc12,"""Include = 'Yes'""")

dissolveFields = ['TITLE_NO']
arcpy.Dissolve_management(fc8,fc14,dissolveFields)

dissolveFields = ['HMLR_Title_No']
arcpy.Dissolve_management(fc12,fc13,dissolveFields)
print 'working shit out'

'''

droppedList = []
addedList = []
changedList = []

UpdateFields = ['TITLE_NO','SHAPE_Area']
#Make A dictionary out of the required LOP plus update fields
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc14,UpdateFields)}

currentFields = ['HMLR_Title_No','SHAPE_Area']
#Update cursor with the checkout and fields for updating
with arcpy.da.SearchCursor(fc13, currentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:

            if updateRow[1] != valueDict[keyValue][0]:
                i = (updateRow[1] - valueDict[keyValue][0])
                areaUpdate = tuple([keyValue,i])

                changedList.append(areaUpdate)

        else:
            droppedList.append(updateRow[0])


UpdateFields = ['HMLR_Title_No','SHAPE_Area']
#Make A dictionary out of the required LOP plus update fields
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc13,UpdateFields)}

currentFields = ['TITLE_NO','SHAPE_Area']
#Update cursor with the checkout and fields for updating
with arcpy.da.SearchCursor(fc14, currentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            continue

        else:
            addedList.append(updateRow[0])



desktopPath = r'C:\Users\UKPXR011\Desktop\Current Work\NPS\NPS_Manchester'

#Open a text document and write the list to it
with open(os.path.join(desktopPath, "droppedList.txt"), "w") as f:
    for item in droppedList:
        f.write("%s\n" % item)


with open(os.path.join(desktopPath, "addedList.txt"), "w") as f:
    for item in addedList:
        f.write("%s\n" % item)



with open(os.path.join(desktopPath, "changedList.txt"), "w") as f:
    for item in changedList:
        f.write("%s\n" % item)

print 'done'

'''