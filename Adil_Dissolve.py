#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     28/01/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

fc1 = r'C:\Users\UKPXR011\Desktop\Paddy_Work\QC Work\Adil\ForPatrick_1.gdb\Plots'
fc2 = r'C:\Users\UKPXR011\Desktop\Paddy_Work\QC Work\Adil\ForPatrick_1.gdb\LOP'
#fc3 = Plots_Ownership
#fc4 = Plots_OwnershipDissolve
#fc5= Plots_Dissolve_Max
Plot_Unique_Field = 'Plot_Number_Unique'
Plot_Unique_Ref_Fields = ['LandReferenceNo','Parish',Plot_Unique_Field]
dissolvefields = ['LandRefNumber','Ownership Reference Number']
dissolvefieldsStats = 'SHAPE_Area MAX'
LopFields = ['OwnershipReferenceNumber','Shape_Area']
PlotFields = ['OwnershipReferenceNumber','Shape_Area']



arcpy.AddField_management(fc1,Plot_Unique_Field,'STRING')

with arcpy.da.UpdateCursor(fc1,Plot_Unique_Ref_Fields ) as updateRows:
    for row in updateRows:
        row[2] = str(row[1]+row[2])
        updateRows.updateRow(row)

del updateRows



hmlrDict = pd.DataFrame.from_records(data=arcpy.da.SearchCursor(HMLRTitles,listfields), columns=listfields).sort_values("created_date").groupby("HMLR_Title_No").last().to_dict()



'''
#Intersect and Dissolve the Plots and Landownership parcels
arcpy.Intersect_analysis([fc1,fc2],fc3, "ALL", "", "INPUT")
arcpy.Dissolve_management(fc3,fc4,dissolvefields)
arcpy.Dissolve_management(fc4,fc5,dissolvefields,dissolvefieldsStats)

CursorJoinFields = ["OwnershipReferenceNumber",'MAX_SHAPE_Area']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc5,CursorJoinFields)}

#Delete the rows where the shape area doesnt match the max area (are not the largest duplicate)
with arcpy.da.UpdateCursor(fc4, ["OwnershipReferenceNumber",'SHAPE_Area']) as updateRows:

    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in valueDict:
            #print 'Made it here 1'
            #print updateRow[1]
            #print valueDict[keyValue][0]
            if updateRow[1] < valueDict[keyValue][0]:
                updateRows.deleteRow()
                #updateRows.updateRow(updateRow)


print 'done'
'''