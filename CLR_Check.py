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
scratch = r'C:\Users\UKPXR011\Desktop\Current Work\2A\LAA\CR035044\Scratch.gdb'
#The feature who geometry will change
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\2A\LAA\Arup_BB_LAA_shapefile2\Scratch.gdb\CLR_44'

fc3 = r'C:\Users\UKPXR011\Desktop\Current Work\2A\LAA\LAA_27072020.gdb\LAPS'

#arcpy.AddField_management(fc1,"Int_Area","DOUBLE")
#arcpy.AddField_management(fc1,"Int_Pct","DOUBLE")

DissolveFields = ['LAPID']
IntersectFields = ['LAPID','SHAPE@AREA']
updateFields = ['LAPID','Int_Area','Int_Pct','SHAPE@AREA']


with arcpy.da.SearchCursor(fc1,['SHAPE@','CLR',"Int_Pct","Int_Area"]) as cursor:
    for row in cursor:
        LAA = str(row[1])
        intersectOutPut = scratch + "\\" + LAA
        arcpy.Select_analysis(fc1, fc6,"""CLR = 'LAA'""")







        '''
        intersectOutPut = scratch + "\\" + str(row[1])
        DissolveOutPut =  scratch + "\\" + str(row[1])+"_Dissolved"
        arcpy.Intersect_analysis([fc3,row[0]],intersectOutPut)
        arcpy.Dissolve_management(intersectOutPut, DissolveOutPut,DissolveFields)

        #Append in old geometry for features
        valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(DissolveOutPut,IntersectFields)}

        with arcpy.da.UpdateCursor(fc3, updateFields) as updateRows:
            for updateRow in updateRows:
                # store the Join value of the row being updated in a keyValue variable
                keyValue = updateRow[0]
                # verify that the keyValue is in the Dictionary
                if keyValue in valueDict:
                    # transfer the value stored under the keyValue from the dictionary to the updated field.
                        updateRow[1] = valueDict[keyValue][0]
                        updateRow[2] = (valueDict[keyValue][0]/updateRow[3])*100
                        updateRows.updateRow(updateRow)

        CLR_Output = intersectOutPut = scratch + "\\" + str(row[1])+"LAPS"

        arcpy.Select_analysis(fc3, fc6,"""Int_Pct IS NOT NULL""")
        with arcpy.da.UpdateCursor(fc3, updateFields) as updateRows:
            for updateRow in updateRows:
                updateRow[1] = None
                updateRow[2] = None
                updateRows.updateRow(updateRow)
'''

print 'Done'