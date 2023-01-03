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

gdb = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\RSZ_Update\Scratch.gdb'
finished = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\RSZ_Update\SLOPS.gdb'
workspace=r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\RSZ_Update\Extract.gdb'

fc1= workspace"\STATUTORY_PROCESSES\LandOwnershipParcels'

fc2= workspace"\STATUTORY_PROCESSES\HMLR_Parcels'

fc3 = workspace +"\STATUTORY_PROCESSES\relLandOwnership_HMLR'

fc4 = GDB +"SLOP_Input_LOP_Temp'

fc5 = GDB +"SLOP_Input_LOP_Temp'

fc6 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Scratch.gdb\New_Safeguarding'

fc7= r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Leeds_Sops_Update\Scratch.gdb\Old_Safeguarding'

fc8 = gdb+"\SG_New_Intersect"

fc9 = gdb+"\SG_New_Intersect_Dissolve"

fc10 =gdb+"\SG_Old_Intersect"

fc11 = gdb+"\SG_Old_Intersect_Dissolve"

fc12 = gdb+"\DissolvedHMLR"

fc13 = gdb+"\SLOP_Input_Hmlr_Intersect"

fc14 = gdb+"\SLOP_Input_Hmlr_Intersect_Dissolve"

fc15 = finished+"\Safeguarding_Land_Ownership_Parcels"

fc16 = gdb+"\Unumbers"

fc17 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\RSZ_Update\Scratch.gdb\RSZ_Merged'

fc18 = gdb+"\RSZ_LOP_Temp"

fc19 = gdb+"\RSZ_LOP"

print "Adding Required Fields"
#Add the fields to hold the globalID
arcpy.AddField_management(fc1, 'LOP_Unique_ID', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc2, 'HMLR_Unique_ID', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc1, 'Include', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc1, 'RSZ', "TEXT","","","", "", "", "", "")
LOP_Unique_Fields = ['GlobalID','LOP_Unique_ID']
HMLR_Unique_Fields = ['GlobalID','HMLR_Unique_ID']

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()



print"Updating Unique Field for LOP and HMLR"
#Update the fields holding the global ID with a cursor
cursor = arcpy.da.UpdateCursor(fc1,LOP_Unique_Fields)
for row in cursor:
    row[1]=str(row[0])
    cursor.updateRow(row)

del cursor

cursor = arcpy.da.UpdateCursor(fc2,HMLR_Unique_Fields)
for row in cursor:
    row[1]=str(row[0])
    cursor.updateRow(row)
del cursor



print "Updating New Safegaurding and LOP"
#Intersect and Dissolve the New Safegaurding Area
arcpy.Intersect_analysis([fc1,fc6],fc8)
arcpy.Dissolve_management(fc8, fc9,'LOP_Unique_ID')

print "Updating Old Safegaurding and LOP"
#Intersect and Dissolve the Old Safegaurding Area
arcpy.Intersect_analysis([fc1,fc7],fc10)
arcpy.Dissolve_management(fc10, fc11,'LOP_Unique_ID')


print "Updating Old Safegaurding and LOP"
#Intersect and Dissolve the Old Safegaurding Area
arcpy.Intersect_analysis([fc1,fc17],fc18)
arcpy.Dissolve_management(fc18, fc19,'LOP_Unique_ID')


JoinFields = ['LOP_Unique_ID','OBJECTID']
Update_Fields = ['LOP_Unique_ID','Include']
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


#add a new field to mark if the parcel is in RSZ but not in the original Safegaurding
JoinFields = ['LOP_Unique_ID','OBJECTID']
Update_Fields = ['LOP_Unique_ID','Include']
# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc19,JoinFields)}
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

edit.stopOperation()
edit.stopEditing(True)

#Select only parcels that are needed for safegaurding
print "Extract LOP's for safeguaridng"
arcpy.Select_analysis(fc1, fc4,"""RSZ = 'Yes' AND Include IS Null""")
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
Dissolve_Fields = ['HMLR_Title_No']
arcpy.Dissolve_management(fc2, fc12,Dissolve_Fields)
arcpy.Intersect_analysis([fc4,fc12],fc13)
Dissolve_Fields = ['HMLR_Title_No','LOP_Unique_ID']
arcpy.Dissolve_management(fc13, fc14,Dissolve_Fields)

print"Removing Intersects smaller than 2m"
#Delete all intersects less than 2m
ownershipFields = ['LOP_Unique_ID','SHAPE_Area']
with arcpy.da.UpdateCursor(fc14, ownershipFields) as updateRows:
    for updateRow in updateRows:
        if updateRow[1]<2:
            updateRows.deleteRow()


#Append in old geometry for features
ownershipFields = ['LOP_Unique_ID','SHAPE@']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc1,ownershipFields)}
print "Updating Geometry"
with arcpy.da.UpdateCursor(fc14, ownershipFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

#Dissolve to combine parcels based on title realtionship
Dissolve_Fields = ['HMLR_Title_No']
print "Dissolving SLOPS"
arcpy.Dissolve_management(fc14, fc15,Dissolve_Fields)

#Select Unumbers out from dataabse
arcpy.Select_analysis(fc4, fc16,"""ExternalReference LIKE 'U%'""")

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



