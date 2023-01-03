#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     26/06/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
arcpy.env.overwriteOutput = True

def concatenate(infeature,uniqueField,concField,writeField):
# Process: Concatenate HMLR Ref
    Delimiter = ','
    Uni_V_Dictionary = {}
    lastid = -1
    lastvalue = ""
    Cur4 = arcpy.da.SearchCursor(infeature,[concField,uniqueField])
    for row in Cur4:
        id = row[1]
        value = row[0]
        Uni_V_Dictionary[id] = value
        if id == lastid:
            value = str(lastvalue) + Delimiter + str(value)
            Uni_V_Dictionary[id] = value
        lastid = id
        lastvalue = value
    del Cur4, row
    cur2 = arcpy.UpdateCursor(infeature)
    for row in cur2:
        id = str(row.getValue(uniqueField))
        row.setValue(writeField, Uni_V_Dictionary[id])
        cur2.updateRow(row)
    del cur2, row

workspace = r'C:\Users\UKPXR011\Desktop\Current Work\PCE Work\PCE_Submission_25062020.gdb'
scratch = r'C:\Users\UKPXR011\Desktop\Current Work\PCE Work\PCESample20200623\Scratch_Script.gdb'

n = 23
n1 = 3
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\PCE Work\Scratch.gdb\Schema_27062020'
fc2 = r'C:\Users\UKPXR011\Desktop\Current Work\PCE Work\Scratch.gdb\Plots'
fc3 = scratch +"\\"+ "Plots_Lops_Temp"
fc4 = scratch +"\\"+ "Plots_Lops"
fc5 = scratch +"\\"+ "Plots_Lops_Dissolved_Lac"
fc6 = scratch +"\\"+ "Plots_Lops_A_B"
fc7 = scratch +"\\"+ "Plots_Lops_A_B_Area"
fc8 = scratch +"\\"+ "Plots_Lops_F"
fc9 = scratch +"\\"+ "Plots_Lops_F_Area"
fc10= scratch +"\\"+ "Plots_Lops_C"
fc11= scratch +"\\"+ "Plots_Lops_C_Area"
fc12 = r'C:\Users\UKPXR011\Desktop\Current Work\PCE Work\Scratch.gdb\Schema_27062020'


plotDissolveFields_Temp = [f.name for f in arcpy.ListFields(fc2)]
del plotDissolveFields_Temp[:n]
del plotDissolveFields_Temp[-n1:]
plotDissolveFields_Temp.pop(1)
plotDissolveFields =[str(f) for f in plotDissolveFields_Temp]
plotDissolveFields.insert(0,"UID")
#print plotDissolveFields


#Intersect and Dissolve lops with Plots
arcpy.Intersect_analysis([fc1,fc2],fc3)
arcpy.Dissolve_management(fc3, fc4,plotDissolveFields)
with arcpy.da.UpdateCursor(fc4,'SHAPE_Area') as updateRows:
    for updateRow in updateRows:
        if updateRow[0] < 2:
            updateRows.deleteRow()

arcpy.AddField_management(fc4,"Plot_Id_Concat","TEXT","","",10000, "", "", "", "")

concatenate(fc4,'UID','UniqueID','Plot_Id_Concat')

#Update Cursor to Schema.

UpdateFields = ['UID','Plot_Id_Concat']
#Make A dictionary out of the required LOP plus update fields
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc4,UpdateFields)}

CurrentFields = ['UID', 'PlotIDs']
#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc12, CurrentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRow[1]= valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

del updateRows


plotDissolveFields = ['UID','LA_Code']
arcpy.Dissolve_management(fc4, fc5,plotDissolveFields)
arcpy.AddField_management(fc5,'LAC_Concat',"TEXT","","",10000, "", "", "", "")
concatenate(fc5,'UID','LA_Code','LAC_Concat')

UpdateFields = ['UID','LAC_Concat']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc5,UpdateFields)}
CurrentFields = ['UID', 'LACRequirements']
#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc12, CurrentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRow[1]= valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

del updateRows


arcpy.Select_analysis(fc4, fc6,"""LA_Code IN( 'A' , 'B' )""")
arcpy.AddField_management(fc6,'A_B_Concat',"TEXT","","",10000, "", "", "", "")

concatenate(fc6,'UID','UniqueID','A_B_Concat')

UpdateFields = ['UID','A_B_Concat']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc6,UpdateFields)}

CurrentFields = ['UID', 'CatABPermPlots']
#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc12, CurrentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRow[1]= valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

arcpy.Dissolve_management(fc6, fc7,'UID')

UpdateFields = ['UID','SHAPE_Area']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc7,UpdateFields)}

CurrentFields = ['UID','AreaOfLand','PermAcquisitionArea']
#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc12, CurrentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRow[2]= (valueDict[keyValue][0]/4046.86)
            updateRows.updateRow(updateRow)



arcpy.Select_analysis(fc4, fc8,"""LA_Code IN( 'C and F' , 'F' )""")
arcpy.AddField_management(fc8,'F_Concat',"TEXT","","",10000, "", "", "", "")

concatenate(fc8,'UID','UniqueID','F_Concat')

UpdateFields = ['UID','F_Concat']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc8,UpdateFields)}

CurrentFields = ['UID', 'CatFTempPlots']
#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc12, CurrentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRow[1]= valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

arcpy.Dissolve_management(fc8, fc9,'UID')

UpdateFields = ['UID','SHAPE_Area']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc9,UpdateFields)}

CurrentFields = ['UID','AreaOfLand','TempAcquisitionArea']
#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc12, CurrentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRow[2]= (valueDict[keyValue][0]/4046.86)
            updateRows.updateRow(updateRow)

arcpy.Select_analysis(fc4, fc10,"""LA_Code IN( 'C and F' , 'C' )""")
arcpy.AddField_management(fc10,'C_Concat',"TEXT","","",10000, "", "", "", "")

concatenate(fc10,'UID','UniqueID','C_Concat')

UpdateFields = ['UID','C_Concat']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc10,UpdateFields)}

CurrentFields = ['UID', 'CatCRightsToBeAcq']
#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc12, CurrentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRow[1]= valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

arcpy.Dissolve_management(fc10, fc11,'UID')

UpdateFields = ['UID','SHAPE_Area']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc11,UpdateFields)}

CurrentFields = ['UID','AreaOfLand','RightsAcquisitionArea']
#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc12, CurrentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            updateRow[2]= (valueDict[keyValue][0]/4046.86)
            updateRows.updateRow(updateRow)


pct_Fields = ['AreaOfLand','PermAcquisitionArea','PercentageOfPermAcq','TempAcquisitionArea','PercentageOfTempAcq']
with arcpy.da.UpdateCursor(fc12, pct_Fields) as updateRows:
    for updateRow in updateRows:

        if updateRow[1] != None:
            i = updateRow[0]
            j = updateRow[1]
            updateRow[2] = (j/i)*100
            if updateRow[2] > 100:
                updateRow[2] = 100

            updateRows.updateRow(updateRow)




        if updateRow[3] != None:
            i = updateRow[0]
            j = updateRow[3]
            updateRow[4] = (j/i)*100
            if updateRow[4] > 100:
                updateRow[4] = 100

            updateRows.updateRow(updateRow)






