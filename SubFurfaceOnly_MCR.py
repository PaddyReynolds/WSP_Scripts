#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     16/03/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
arcpy.env.overwriteOutput = True

#GDDs
extract = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\SubSurface_Only\SubSurface_Only.gdb\\'
scratch = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\SubSurface_Only\Scratch.gdb\\'

#Feature Classes
fc1 = scratch + 'New_Safeguarding'
fc2 = scratch + 'New_Safeguarding_temp'
fc3 = scratch + 'Old_Safeguarding'
fc4 = scratch + 'Old_Safeguarding_Temp'
fc5 = scratch + 'SG_Merged'
fc6 = extract + 'HMLR_Parcels'
fc7 = scratch +'HMLR_Dissolved'
fc8 = scratch +'HMLR_Dissolved_SG_Temp'
fc9 = scratch +'HMLR_Dissolved_SG'
fc10 = scratch +'HMLR_Dissolved_SG_Zone_Count'
fc11 = scratch +'HMLR_Sub_Only'
fc12 = extract + 'Safeguarding_Land_Ownership_Parcels'
fc13 = scratch +'SLOP_SG_Temp'
fc14 = scratch +'SLOP_Dissolved_SG'
fc15 = scratch +'SLOP_Dissolved_SG_Zone_Count'
fc16 = scratch +'SLOP_Sub_Only'
fc17 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\SubSurface_Only\LOPS.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'
fc18 = scratch +'Unumbers'



#Dissolve HMLR to make it Multipart
arcpy.Dissolve_management(fc6, fc7,'HMLR_Title_No')


#Select Unumbers out from database
arcpy.Select_analysis(fc17, fc18,"""ExternalReference LIKE 'U%'""")
Unumbers=[]
ownershipFields = ['ExternalReference','Shape@']
with arcpy.da.SearchCursor(fc16,ownershipFields) as cursor:
    for row in cursor:
        Unumbers.append(row)

del cursor

#Append in Unumbers to HMLR dissolve
Fieldlist= ['HMLR_Title_No','Shape@']
with arcpy.da.InsertCursor(fc7, Fieldlist) as cursor:
    for row in Unumbers:
        cursor.insertRow(row)

#Select out the old and new SG zones we want and merge them into one layer
arcpy.Select_analysis(fc1, fc2,"""Zone_Type IN( 'EHPZ1' , 'EHPZ2' , 'EHPZ3' , 'RSZ' , 'SGSub' , 'SGSur' )""")
arcpy.Select_analysis(fc3, fc4,"""Zone_Type IN( 'EHPZ1' , 'EHPZ2' , 'EHPZ3' , 'RSZ' , 'SGSub' , 'SGSur' )""")
arcpy.Merge_management([fc2, fc4],fc5)

#Intersect and Dissolve the HMLR and safeguarding areas, Dissolve first by title number and zone type then dissolve again to get a count of zones to keep only the titles that fall in a single zone
arcpy.Intersect_analysis([fc5,fc7],fc8)
arcpy.Dissolve_management(fc8, fc9,['HMLR_Title_No','Zone_Type'])
arcpy.Dissolve_management(fc9, fc10,['HMLR_Title_No'],'Zone_Type COUNT')

#Add a field to show thoes fields unique to SubSurface Onlu
arcpy.AddField_management(fc9, 'Sub_Only', "TEXT","","","", "", "", "", "")

#Make a dictionary of thoes titles that only intersect one zone type
titleFields = ['HMLR_Title_No','COUNT_Zone_Type']
where_clause = """COUNT_Zone_Type = 1"""
# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc10,titleFields,where_clause)}

with arcpy.da.UpdateCursor(fc9,['HMLR_Title_No','Sub_Only'],"""Zone_Type ='SGSub'""") as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = 'Yes'
            updateRows.updateRow(updateRow)
        else:
            pass
del valueDict,updateRows

arcpy.Select_analysis(fc9, fc11,"""Sub_Only ='Yes'""")

#Do the same again but for SLOPS

#Intersect and Dissolve the HMLR and safeguarding areas, Dissolve first by title number and zone type then dissolve again to get a count of zones to keep only the titles that fall in a single zone
arcpy.Intersect_analysis([fc5,fc12],fc13)
arcpy.Dissolve_management(fc13, fc14,['OwnershipReferenceNumber','Zone_Type'])
arcpy.Dissolve_management(fc14, fc15,['OwnershipReferenceNumber'],'Zone_Type COUNT')

#Add a field to show thoes fields unique to SubSurface Onlu
arcpy.AddField_management(fc14, 'Sub_Only', "TEXT","","","", "", "", "", "")

#Make a dictionary of thoes titles that only intersect one zone type
titleFields = ['OwnershipReferenceNumber','COUNT_Zone_Type']
where_clause = """COUNT_Zone_Type = 1"""
# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc15,titleFields,where_clause)}

with arcpy.da.UpdateCursor(fc14,['OwnershipReferenceNumber','Sub_Only'],"""Zone_Type ='SGSub'""") as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = 'Yes'
            updateRows.updateRow(updateRow)
        else:
            pass
del valueDict,updateRows

arcpy.Select_analysis(fc14, fc16,"""Sub_Only ='Yes'""")



