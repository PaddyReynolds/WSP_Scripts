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
gdb = r'C:\Users\UKPXR011\Desktop\Paddy_Work\GSSGISK_2631\Scratch.gdb'
finished = r'C:\Users\UKPXR011\Desktop\Paddy_Work\GSSGISK_2631\SLOPS.gdb'
workspace= r'C:\Users\UKPXR011\Desktop\Paddy_Work\GSSGISK_2631\HMLR_Update.gdb'

fc1= r'C:\Users\UKPXR011\Desktop\Paddy_Work\GSSGISK_2631\HMLR_Update.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'

fc2= r'C:\Users\UKPXR011\Desktop\Paddy_Work\GSSGISK_2631\HMLR_Update.gdb\STATUTORY_PROCESSES\HMLR_Parcels'

fc3 = r'C:\Users\UKPXR011\Desktop\Paddy_Work\GSSGISK_2631\HMLR_Update.gdb\STATUTORY_PROCESSES\relLandOwnership_HMLR'

fc4 = gdb + '\\LOP_1'

print "Adding Required Fields"
#Add the fields to hold the globalID
arcpy.AddField_management(fc1, 'LOP_Unique_ID', "TEXT","","","", "", "", "", "")
LOP_Unique_Fields = ['GlobalID','LOP_Unique_ID']


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

edit.stopOperation()
edit.stopEditing(True)

arcpy.Select_analysis(fc1, fc4)

relatesList=[]
Fieldlist = ['LOP_Unique_ID','Relate','Relate_Count']

arcpy.AddField_management(fc4, 'Relate', "TEXT","","","", "", "", "", "")
arcpy.AddField_management(fc4, 'Relate_Count', "TEXT","","","", "", "", "", "")

print "Counting Relates"
#Make a list of relates table
for row in arcpy.da.SearchCursor(fc3, ['LOwnGlobalID']):
    relatesList.append(row[0])

#Creat a dictionary where the key value is the global ID and the value is the number of times it appears in a list
relates_Dict_C = Counter(relatesList)
relates_Dict = dict(relates_Dict_C)

#Check how many relationships each parcel has then copy that parcel x number of times so it exists in the featureclass as many times as it has relationships
print "Creating one Parcel for each parcel relate"

with arcpy.da.UpdateCursor(fc4, Fieldlist) as cursor:
    for row in cursor:

        keyValue = row[0]
        if keyValue in relates_Dict:

            row[1] = 'Yes'
            row[2] = str(relates_Dict[keyValue])
            cursor.updateRow(row)
        else:
            row[1] = 'No'


print 'Done'
print 'Not a Chance that worked'










