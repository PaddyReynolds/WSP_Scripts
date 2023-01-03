#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKDXE008
#
# Created:     20/01/2021
# Copyright:   (c) UKDXE008 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
from collections import Counter

Checkout = r"C:\Users\ukdxe008\Documents\Projects\HS2 Phase 2 b\shapefile\Matt_B_20210119\OutPut.gdb"

#Checkout_Licence = r"C:\Users\ukdxe008\Documents\Projects\HS2 Phase 2 b\Amends\AmendsFolder_202101171633\DE_Checkout_20210117_3\AmendsFolder_202101171633\DE_Checkout_20210117_3.gdb\STATUTORY_PROCESSES\AccessLicences"
Template = r"C:\Users\ukdxe008\Documents\Projects\HS2 Phase 2 b\shapefile\Matt_B_20210119\OutPut.gdb\Template"

#Noida_AL_Edits_AL = r"C:\Users\ukdxe008\Documents\Projects\HS2 Phase 2 b\Amends\AmendsFolder_202101171633\DE_Errors.gdb\AL_New_Area"
List = r"C:\Users\ukdxe008\Documents\Projects\HS2 Phase 2 b\shapefile\Matt_B_20210119\Working_Data.gdb\List"
All_LOPS_Checkout = r"C:\Users\ukdxe008\Documents\Projects\HS2 Phase 2 b\shapefile\Matt_B_20210119\Working_Data.gdb\All_LOPs"


# ________________________________________
relatesList=[]
Fieldlist = [f.name for f in arcpy.ListFields(Template)]
Fieldlist.append('SHAPE@')

print "Counting Relates"
#Make a list of relates table
for row in arcpy.da.SearchCursor(List, ['OwnershipReferenceNumber']):
    relatesList.append(row[0])

print relatesList
#Creat a dictionary where the key value is the global ID and the value is the number of times it appears in a list
relates_Dict_C = Counter(relatesList)
relates_Dict = dict(relates_Dict_C)

#print "List"
#print Noida_AL_Edits_LOP
#print 'relates List'
#print relatesList
#print 'relates dict'
#print relates_Dict
#print 'relates dict C'
#print relates_Dict_C

#Check how many relationships each parcel has then copy that parcel x number of times so it exists in the featureclass as many times as it has relationships
print "Creating one Parcel for each parcel relate"
with arcpy.da.SearchCursor(All_LOPS_Checkout, Fieldlist) as scur:
    with arcpy.da.InsertCursor(Template, Fieldlist) as cursor:
        for row in scur:
            keyValue = str(row[18])
            print 'Keyvalue'
            print keyValue
            print 'relates Dict'
            print relates_Dict
            if keyValue in relates_Dict:

                insertCounter = (relates_Dict[keyValue])-1
                print insertCounter
                if insertCounter == 0:
                    print "insert work"
                    pass

                else:


                    for i in range(insertCounter):
                        print "insert work 2"
                        cursor.insertRow(row)

print 'test run'
print 'fin'
#_____________________________________________-

