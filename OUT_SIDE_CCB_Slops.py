#-------------------------------------------------------------------------------
# Name:        module2
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
fc2 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\MCR_outside_CCB\Scratch.gdb\HMLR_Single_Part_SG'
fc3 = gdb + 'HMLR_Extract'
fc4 = gdb + 'HMLR_Extract_Temp'
fc13 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\MCR_outside_CCB\DE_SGCreation_Checkout_20200420.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'
fc5 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\MCR_outside_CCB\DE_SGCreation_Checkout_20200420.gdb\STATUTORY_PROCESSES\relLandOwnership_HMLR'
fc6 = gdb +'SLOP_Input_Lop'
fc7 = gdb +'SLOP_Input_Lop_Temp'
fc8 = gdb +'DissolvedHMLR'
fc9 = gdb +'SLOP_Input_Hmlr_Intersect'
fc10 = gdb +'SLOP_Input_Hmlr_Intersect_Dissolve'
fc11 = finished +'Safeguarding_Land_Ownership_Parcels'
fc12 = gdb +'Unumbers'


#arcpy.AddField_management(fc1, 'HMLR_Unique_ID', "TEXT","","","", "", "", "", "")
#arcpy.AddField_management(fc1, 'Include', "TEXT","","","", "", "", "", "")
#arcpy.AddField_management(fc13, 'LOP_Unique_ID', "TEXT","","","", "", "", "", "")
#arcpy.AddField_management(fc13, 'Include', "TEXT","","","", "", "", "", "")


edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

JoinFields = ['HMLR_Title_No','OBJECTID']
Update_Fields = ['HMLR_Title_No','Include']
# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc2,JoinFields)}
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


HMLR_Unique_Fields = ['GlobalID','HMLR_Unique_ID','Include']
cursor = arcpy.da.UpdateCursor(fc1,HMLR_Unique_Fields)
for row in cursor:
    if row[2] == 'Yes':
        row[1]=str(row[0])
        cursor.updateRow(row)

    else:
        pass
del cursor

edit.stopOperation()
edit.stopEditing(True)

arcpy.Select_analysis(fc1, fc3,"""Include = 'Yes'""")
arcpy.Select_analysis(fc3, fc4)

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

LOP_Unique_Fields = ['GlobalID','LOP_Unique_ID']
cursor = arcpy.da.UpdateCursor(fc13,LOP_Unique_Fields)
for row in cursor:
        row[1]=str(row[0])
        cursor.updateRow(row)
del cursor


edit.stopOperation()
edit.stopEditing(True)

relates_list= []
for row in arcpy.da.SearchCursor(fc4, ['HMLR_Unique_ID']):
    relates_list.append(row[0])

LOP_List = []
with arcpy.da.SearchCursor(fc5,['LOwnGlobalID','Hmlr_GlobalID'])as cursor:
    for row in cursor:
        if row[1] in relates_list:
            LOP_List.append(row[0])
print LOP_List

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

LOP_Unique_Fields = ['LOP_Unique_ID','Include']
cursor = arcpy.da.UpdateCursor(fc13,LOP_Unique_Fields)
for row in cursor:
    if row[0] in LOP_List:
        row[1]='Yes'
        cursor.updateRow(row)

edit.stopOperation()
edit.stopEditing(True)

arcpy.Select_analysis(fc13, fc6,"""Include = 'Yes'""")
fc7 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\MCR_outside_CCB\Scratch.gdb\\SLOP_Input_Lop_Temp'
arcpy.Select_analysis(fc6, fc7)


relatesList=[]
Fieldlist = [f.name for f in arcpy.ListFields(fc6)]
Fieldlist.append('SHAPE@')

print "Counting Relates"
#Make a list of relates table
for row in arcpy.da.SearchCursor(fc5, ['LOwnGlobalID']):
    relatesList.append(row[0])

#Creat a dictionary where the key value is the global ID and the value is the number of times it appears in a list
relates_Dict_C = Counter(relatesList)
relates_Dict = dict(relates_Dict_C)

#Check how many relationships each parcel has then copy that parcel x number of times so it exists in the featureclass as many times as it has relationships
print "Creating one Parcel for each parcel relate"
with arcpy.da.SearchCursor(fc7, Fieldlist) as scur:
    with arcpy.da.InsertCursor(fc6, Fieldlist) as cursor:
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
arcpy.Dissolve_management(fc2, fc8,Dissolve_Fields)
arcpy.Intersect_analysis([fc6,fc8],fc9)
Dissolve_Fields = ['HMLR_Title_No','LOP_Unique_ID']
arcpy.Dissolve_management(fc9, fc10,Dissolve_Fields)

print"Removing Intersects smaller than 2m"
#Delete all intersects less than 2m
ownershipFields = ['LOP_Unique_ID','SHAPE_Area']
with arcpy.da.UpdateCursor(fc10, ownershipFields) as updateRows:
    for updateRow in updateRows:
        if updateRow[1]<2:
            updateRows.deleteRow()


#Append in old geometry for features
ownershipFields = ['LOP_Unique_ID','SHAPE@']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc13,ownershipFields)}
print "Updating Geometry"
with arcpy.da.UpdateCursor(fc10, ownershipFields) as updateRows:
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
arcpy.Dissolve_management(fc10, fc11,Dissolve_Fields)




'''
#Select Unumbers out from dataabse
arcpy.Select_analysis(fc7, fc12,"""ExternalReference LIKE 'U%'""")

Unumbers=[]
ownershipFields = ['ExternalReference','Shape@']
with arcpy.da.SearchCursor(fc12,ownershipFields) as cursor:
    for row in cursor:
        Unumbers.append(row)

del cursor

print "Ther are " + str(len(Unumbers)) + " Unregistered Parcels"
#Use an Update Cursor to Append In Unumbers
print "Appening In Unregistered Land"
Fieldlist= ['HMLR_Title_No','Shape@']
with arcpy.da.InsertCursor(fc11, Fieldlist) as cursor:
    for row in Unumbers:
        cursor.insertRow(row)
'''
#Add a Field for an update Cursor
arcpy.AddField_management(fc11, 'OwnershipReferenceNumber', "SHORT","","","", "", "", "", "")


