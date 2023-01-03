#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     19/02/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from collections import Counter

arcpy.env.overwriteOutput = True

gdb = r'C:\Users\ukdxe008\Desktop\Safeguarding_2b_2019_2020\Scripts\SLOP_Creation\M2M3_Script_Runs\Updating_Scripts\Scratch.gdb'
finished = r'C:\Users\ukdxe008\Desktop\Safeguarding_2b_2019_2020\Scripts\SLOP_Creation\M2M3_Script_Runs\Updating_Scripts\SLOPs.gdb'
workspace=r'C:\Users\ukdxe008\Desktop\Safeguarding_2b_2019_2020\Scripts\SLOP_Creation\M2M3_Checkout_20200420\DE_SGCreation_Checkout_20200420.gdb'

fc1= r'C:\Users\ukdxe008\Desktop\Safeguarding_2b_2019_2020\Scripts\SLOP_Creation\M2M3_Checkout_20200420\DE_SGCreation_Checkout_20200420.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'

fc2= r'C:\Users\ukdxe008\Desktop\Safeguarding_2b_2019_2020\Scripts\SLOP_Creation\M2M3_Checkout_20200420\DE_SGCreation_Checkout_20200420.gdb\STATUTORY_PROCESSES\HMLR_Parcels'

fc3 = r'C:\Users\ukdxe008\Desktop\Safeguarding_2b_2019_2020\Scripts\SLOP_Creation\M2M3_Checkout_20200420\DE_SGCreation_Checkout_20200420.gdb\STATUTORY_PROCESSES\relLandOwnership_HMLR'

fc4 = gdb + '\SLOP_Input_LOP'

fc5 = gdb + '\SLOP_Input_LOP_Temp'

fc6 = r'C:\Users\ukdxe008\Desktop\Safeguarding_2b_2019_2020\Scripts\SLOP_Creation\M2M3_Script_Runs\Creation_Run\SG_Data_Exports.gdb\SG_New'

fc7 = r'C:\Users\ukdxe008\Desktop\Safeguarding_2b_2019_2020\Scripts\SLOP_Creation\M2M3_Script_Runs\Creation_Run\SG_Data_Exports.gdb\SG_OLD'

fc8 = gdb+"\SG_New_Intersect"

fc9 = gdb+"\SG_New_Intersect_Dissolve"

fc10 =gdb+"\SG_Old_Intersect"

fc11 = gdb+"\SG_Old_Intersect_Dissolve"

fc12 = gdb+"\DissolvedHMLR"

fc13 = gdb+"\SLOP_Input_Hmlr_Intersect"

fc14 = gdb+"\SLOP_Input_Hmlr_Intersect_Dissolve"

fc15 = finished+"\Safeguarding_Land_Ownership_Parcels"

fc16 = gdb+"\Unumbers"

fc17 = gdb+"\RelLOP_HMLR_Copy"

fc18 = gdb+"\SLOP_WithRelate"

print "Adding Required Fields"
#Add the fields to hold the globalID
arcpy.AddField_management(fc1, 'LOP_Unique_ID', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc2, 'HMLR_Unique_ID', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc1, 'Include', "TEXT","","","", "", "", "", "")
LOP_Unique_Fields = ['GlobalID','LOP_Unique_ID','Include']
HMLR_Unique_Fields = ['GlobalID','HMLR_Unique_ID']

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

print "Updating New Safegaurding and LOP"
#Intersect and Dissolve the New Safegaurding Area
arcpy.Intersect_analysis([fc1,fc6],fc8)
arcpy.Dissolve_management(fc8, fc9,'OwnershipReferenceNumber')

print "Updating Old Safegaurding and LOP"
#Intersect and Dissolve the Old Safegaurding Area
arcpy.Intersect_analysis([fc1,fc7],fc10)
arcpy.Dissolve_management(fc10, fc11,'OwnershipReferenceNumber')

JoinFields = ['OwnershipReferenceNumber','OBJECTID']
Update_Fields = ['OwnershipReferenceNumber','Include']
# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc9,JoinFields)}
valueDict1 = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc11,JoinFields)}
print "Updating Parcels required for safegaurding"
#Update the Inlcude field to show which LOPs were intersected by old and new safeguarding
with arcpy.da.UpdateCursor(fc1, Update_Fields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = 'Yes'
            updateRows.updateRow(updateRow)

        if keyValue in valueDict1:

            # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = 'Yes'
            updateRows.updateRow(updateRow)

print"Updating Unique Field for LOP and HMLR"
#Update the fields holding the global ID with a cursor
cursor = arcpy.da.UpdateCursor(fc1,LOP_Unique_Fields)
for row in cursor:
    if row[2] == 'Yes':
        row[1]=str(row[0])
        cursor.updateRow(row)

    else:
        pass
del cursor

cursor = arcpy.da.UpdateCursor(fc2,HMLR_Unique_Fields)
for row in cursor:
    row[1]=str(row[0])
    cursor.updateRow(row)
del cursor


edit.stopOperation()
edit.stopEditing(True)

#Select only parcels that are needed for safegaurding
print "Extract LOP's for safeguaridng"
arcpy.Select_analysis(fc1, fc4,"""Include = 'Yes'""")
arcpy.Select_analysis(fc4, fc5)

relatesList=[]
Fieldlist = [f.name for f in arcpy.ListFields(fc4)]
Fieldlist.append('SHAPE@')

print "Counting Relates"
#Make a list of relates table
for row in arcpy.da.SearchCursor(fc3, ['LOwnGlobalID']):
    relatesList.append(row[0])

#Creat a dictionary where the key value is the global ID and the value is the number of times it appears in a list
relates_Dict_C = Counter(relatesList)
relates_Dict = dict(relates_Dict_C)

#Check how many relationships each parcel has then copy that parcel x number of times so it exists in the featureclass as many times as it has relationships
print "Creating one Parcel for each parcel relate"
with arcpy.da.SearchCursor(fc5, Fieldlist) as scur:
    with arcpy.da.InsertCursor(fc4, Fieldlist) as cursor:
        for row in scur:
            keyValue = str(row[25])

            if keyValue in relates_Dict:

                insertCounter = (relates_Dict[keyValue])-1

                if insertCounter == 0:

                    pass

                else:


                    for i in range(insertCounter):
                        cursor.insertRow(row)


#Intersect and Dissolve to get all title and parcel relations
print "Intersect Dissolve to get title and LOP relationships"
Dissolve_Fields = ['HMLR_Title_No','HMLR_Unique_ID']
arcpy.Dissolve_management(fc2, fc12,Dissolve_Fields)
arcpy.Intersect_analysis([fc4,fc12],fc13)
Dissolve_Fields = ['HMLR_Title_No','HMLR_Unique_ID','LOP_Unique_ID']
arcpy.Dissolve_management(fc13, fc14,Dissolve_Fields)
addMergeField = arcpy.AddField_management(fc14,"Unique_ID_Merge","TEXT","","","", "", "", "", "")
fields = ['HMLR_Unique_ID','LOP_Unique_ID','Unique_ID_Merge']
with arcpy.da.UpdateCursor(fc14,fields) as cursor:
    for row in cursor:
        row[2] = (row[1]+row[0])

        cursor.updateRow(row)
print 'unique ID field merged'


# add fields to the relate table
select = arcpy.TableToTable_conversion(fc3,gdb,"RelLOP_HMLR_Copy")
print 'select complete'
arcpy.AddField_management(fc17, 'LOP_Glob_Unique_ID', "TEXT","","",500, "", "", "", "")
arcpy.AddField_management(fc17, 'HMLR_Glob_Unique_ID', "TEXT","","",500, "", "", "", "")
arcpy.AddField_management(fc17, 'Glob__Merge_Unique_ID', "TEXT","","",1000, "", "", "", "")
# Update the fields now added with the global id fields
field = ['LOwnGlobalID','Hmlr_GlobalID','LOP_Glob_Unique_ID','HMLR_Glob_Unique_ID','Glob__Merge_Unique_ID']
with arcpy.da.UpdateCursor(fc17, field) as cursor:
    for row in cursor:
        row[2] = row[0]
        row[3] = row[1]
        row[4] = (row[2]+row[3])

        cursor.updateRow(row)

print 'update the relates table'

# join relates table and feature to extract only parcels with a relate present
joinfield = arcpy.JoinField_management(fc14,"Unique_ID_Merge",fc17,"Glob__Merge_Unique_ID","Glob__Merge_Unique_ID")
Select_Related_Parcels = arcpy.Select_analysis(fc14,fc18,"""Glob__Merge_Unique_ID is not NULL""")
print ' Selected_Related Parcels'
Dissolve_Fields = ['HMLR_Title_No']

#Append in old geometry for features
ownershipFields = ['LOP_Unique_ID','SHAPE@']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc1,ownershipFields)}
print "Updating Geometry"
with arcpy.da.UpdateCursor(fc18, ownershipFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

# dissolve to combine parcels on title
arcpy.Dissolve_management(fc18,fc15,Dissolve_Fields)
print 'SLOP titles created'

#Select Unumbers out from dataabse
arcpy.Select_analysis(fc5, fc16,"""ExternalReference LIKE 'U%'""")

Unumbers=[]
ownershipFields = ['ExternalReference','Shape@']
with arcpy.da.SearchCursor(fc16,ownershipFields) as cursor:
    for row in cursor:
        Unumbers.append(row)

del cursor

print "Ther are " + str(len(Unumbers)) + " Unregistered Parcels"
#Use an Update Cursor to Append In Unumbers
print "Appening In Unregistered Land"
Fieldlist= ['HMLR_Title_No','Shape@']
with arcpy.da.InsertCursor(fc15, Fieldlist) as cursor:
    for row in Unumbers:
        cursor.insertRow(row)

#Add a Field for an update Cursor
arcpy.AddField_management(fc15, 'OwnershipReferenceNumber', "SHORT","","","", "", "", "", "")

'''
#Auto Number Plots from South to North
arcpy.AddMessage("Auto Numbering Plots from South to North")
cursor = arcpy.SearchCursor(fc15)
for row1 in cursor:
    coords = [[round(i[0],0),i[1]] for i in arcpy.da.SearchCursor(fc15,['SHAPE@Y','OID@'])]
    coords.sort(key=lambda k: (k[0]),reverse=False)
    order = [i[1] for i in coords]
    d = {k:v for (v,k) in list(enumerate(order))}
    with arcpy.da.UpdateCursor(fc15,["OID@",'OwnershipReferenceNumber']) as cursor:
        for row in cursor:
            row[1] = int(d[row[0]]+1)
            cursor.updateRow(row)


'''
print ("Done")



