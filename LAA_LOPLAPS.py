#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     28/07/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

#The GDB which the feature whos geometry will change lives
scratch = r'C:\Users\UKPXR011\Desktop\Current Work\2A\LAA\LAA_Update_20012021\Scratch.gdb'
outFolder = r'C:\Users\UKPXR011\Desktop\Current Work\2A\LAA\LAA_Update_20012021\\'
workspace = r'C:\Users\UKPXR011\Desktop\Current Work\2A\LAA\LAA_Update_20012021\LAA_Update_19012021.gdb'
output_GDB = r'C:\Users\UKPXR011\Desktop\Current Work\2A\LAA\LAA_Update_20012021\New File Geodatabase.gdb\\'

arcpy.env.overwriteOutput = True
arcpy.env.workspace = scratch

#The feature who geometry will change
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\2A\LAA\LAA_Update_20012021\Scratch.gdb\CLRS'

fc3 = r'C:\Users\UKPXR011\Desktop\Current Work\2A\LAA\LAA_Update_20012021\LAA_Update_19012021.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'

arcpy.AddField_management(fc3,"CLR_Ref","TEXT")
arcpy.AddField_management(fc3,"LAA_ID_Ref","TEXT")
arcpy.AddField_management(fc3,"Int_Area","DOUBLE")
arcpy.AddField_management(fc3,"Int_Pct","DOUBLE")

DissolveFields = ['OwnershipReferenceNumber','CLRID','LAA_ID']
IntersectFields = ['OwnershipReferenceNumber','SHAPE@AREA','CLRID','LAA_ID']
updateFields = ['OwnershipReferenceNumber','Int_Area','Int_Pct','SHAPE@AREA','CLR_Ref','LAA_ID_Ref']

#Start Edditing
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

LAP_Area_Fields = ['OwnershipReferenceNumber','SHAPE@AREA']
Lap_Area_Dict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc3,LAP_Area_Fields)}

counter = 0

with arcpy.da.SearchCursor(fc1,['SHAPE@','LAA_ID']) as cursor:

    for row in cursor:
        print counter
        LAA = str(row[1])
        CLR_Individual = scratch + "\\" + LAA
        query = "LAA_ID =" + "'" + LAA + "'"
        arcpy.Select_analysis(fc1, CLR_Individual,query)
        intersectOutPut = scratch + "\\" + LAA + "Intersect"
        DissolveOutPut =  scratch + "\\" + LAA + "_Dissolved"
        arcpy.Intersect_analysis([fc3,CLR_Individual],intersectOutPut)

        arcpy.Dissolve_management(intersectOutPut, DissolveOutPut,DissolveFields)
        #Join Back original Area field to dissolve output
        arcpy.AddField_management(DissolveOutPut,"OG_Area","DOUBLE")
        Lap_Area_Fields = ['OwnershipReferenceNumber','SHAPE@AREA','OG_Area']
        with arcpy.da.UpdateCursor(DissolveOutPut,Lap_Area_Fields) as updateRows:
            for updateRow in updateRows:
                keyValue = updateRow[0]
                if keyValue in Lap_Area_Dict:
                    updateRow[2] = Lap_Area_Dict[keyValue][0]
                    updateRows.updateRow(updateRow)

        del updateRows

        #Make a query which only adds intersects greater than 1m or if the parcel is less than 1m2
        expression = """Shape_Area > 1 OR OG_Area <= 1"""

        #Append in old geometry for features
        valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(DissolveOutPut,IntersectFields,expression)}

        with arcpy.da.UpdateCursor(fc3, updateFields) as updateRows:
            for updateRow in updateRows:
                # store the Join value of the row being updated in a keyValue variable
                keyValue = updateRow[0]
                # verify that the keyValue is in the Dictionary
                if keyValue in valueDict:
                    # transfer the value stored under the keyValue from the dictionary to the updated field.
                        updateRow[1] = valueDict[keyValue][0]
                        updateRow[2] = (valueDict[keyValue][0]/updateRow[3])*100
                        updateRow[4] = valueDict[keyValue][1]
                        updateRow[5] = valueDict[keyValue][2]
                        updateRows.updateRow(updateRow)

        del valueDict, updateRows

        CLR_Output = intersectOutPut = scratch + "\\" + LAA +"LAPS"
        CLR_OutputDissolved = intersectOutPut = scratch + "\\" + LAA +"_LAPS_Dissolved"
        DissolveFields2 = ['OwnershipReferenceNumber','Int_Area','Int_Pct','CLR_Ref','LAA_ID_Ref']
        arcpy.Select_analysis(fc3, CLR_Output,"""Int_Pct IS NOT NULL""")
        arcpy.Dissolve_management(CLR_Output, CLR_OutputDissolved,DissolveFields2)
        LAA_SDE = output_GDB + LAA + "_SDE"
        DissolveFields3 = ['CLR_Ref','LAA_ID_Ref']
        arcpy.Dissolve_management(CLR_OutputDissolved,LAA_SDE,DissolveFields3)
        outxls = outFolder + LAA +".xls"
        arcpy.TableToExcel_conversion(CLR_OutputDissolved, outxls)
        with arcpy.da.UpdateCursor(fc3, updateFields) as updateRows:
            for updateRow in updateRows:
                updateRow[1] = None
                updateRow[2] = None
                updateRow[4] = None
                updateRow[5] = None
                updateRows.updateRow(updateRow)

        del updateRows
        counter = counter + 1


edit.stopOperation()
edit.stopEditing(True)

print 'Done'