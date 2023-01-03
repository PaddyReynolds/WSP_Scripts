#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     20/04/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from collections import Counter

arcpy.env.overwriteOutput = True
gdb = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\MCR_outside_CCB\Scratch.gdb\\'
finished = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\MCR_outside_CCB\Slops.gdb\\'
workspace=r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\MCR_outside_CCB\DE_SGCreation_Checkout_20200420.gdb'

fc1 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\MCR_outside_CCB\DE_SGCreation_Checkout_20200420.gdb\STATUTORY_PROCESSES\HMLR_Parcels'
fc2 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\MCR_outside_CCB\DE_SGCreation_Checkout_20200420.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'
fc3 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\MCR_outside_CCB\DE_SGCreation_Checkout_20200420.gdb\STATUTORY_PROCESSES\relLandOwnership_HMLR'
fc4 = gdb +'SLOP_Input_Hmlr_Intersect_Non_Spatial'
fc5 = gdb +'SLOP_Input_Hmlr_Intersect_Non_Spatial_Dissovle'


arcpy.AddField_management(fc1, 'HMLR_Unique_ID', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc2, 'LOP_Unique_ID', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc13, 'OG_Area', "Double","","","", "", "", "", "")


Dissolve_Fields_Non_Spatial = ['HMLR_Unique_ID','LOP_Unique_ID']
arcpy.Intersect_analysis([fc1,fc2],fc4)
arcpy.Dissolve_management(fc4, fc5,Dissolve_Fields_Non_Spatial)

ownershipFields = ['LOP_Unique_ID','SHAPE_Area']
with arcpy.da.UpdateCursor(fc5, ownershipFields) as updateRows:
    for updateRow in updateRows:
        if updateRow[1]<2:
            updateRows.deleteRow()


#Append in old geometry for features
relationship_Fields = ['LOwnGlobalID','Hmlr_GlobalID']
ownership_Fileds = ['LOP_Unique_ID','HMLR_Unique_ID']
#valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc5,ownershipFields)}
LownGlobalID = []
relate_List = []
with arcpy.da.SearchCursor(fc5, ownership_Fileds) as cursor:
    for row in cursor:
        relate_List.append(row)

del cursor


with arcpy.da.SearchCursor(fc3, relationship_Fields) as cursor:
    for row in cursor:
        if row in relate_List:
            pass

        else:
            LownGlobalID.append(row)


print len(LownGlobalID), LownGlobalID[0]



