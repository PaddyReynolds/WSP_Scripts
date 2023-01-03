#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     23/04/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from collections import Counter

arcpy.env.overwriteOutput = True

gdb = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\SLOP_Fix_23_04_2020\Scratch1\Scratch1_1.gdb'
finished = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\SLOP_Fix_23_04_2020\Scratch1.gdb\Scratch1_1.gdb'
workspace=r'C:\Users\UKPXR011\Desktop\Paddy_Work\GSSGISK_2631\HMLR_Update.gdb'

fc1= workspace + '\STATUTORY_PROCESSES\LandOwnershipParcels'

fc2= workspace + '\STATUTORY_PROCESSES\HMLR_Parcels'

fc3 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\SLOP_Fix_23_04_2020\DE_Export_SG_Creation\DE_Export_SG_Creation.gdb\STATUTORY_PROCESSES\relLandOwnership_HMLR'

fc4 = gdb + '\SLOP_Input_LOP'

fc5 = gdb + '\SLOP_Input_LOP_Temp'

fc6 = gdb + 'New_Safeguarding'

fc7= gdb + 'Old_Safeguarding'

fc8 = gdb+"\SG_New_Intersect"

fc9 = gdb+"\SG_New_Intersect_Dissolve"

fc10 =gdb+"\SG_Old_Intersect"

fc11 = gdb+"\SG_Old_Intersect_Dissolve"

fc12 = gdb+"\DissolvedHMLR"

fc13 = gdb+"\SLOP_Input_Hmlr_Intersect"

fc14 = gdb+"\SLOP_Input_Hmlr_Intersect_Dissolve"

fc15 = finished+"\Safeguarding_Land_Ownership_Parcels"

fc16 = gdb+"\Unumbers"


relatesList=[]
Fieldlist = [f.name for f in arcpy.ListFields(fc4)]
Fieldlist.append('SHAPE@')

print "Counting Relates"
#Make a list of relates table
fc3 = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\SLOP_Fix_23_04_2020\DE_Export_SG_Creation\DE_Export_SG_Creation.gdb\STATUTORY_PROCESSES\relLandOwnership_HMLR'
for row in arcpy.da.SearchCursor(fc3, ['LOwnGlobalID']):
    relatesList.append(row[0])

#Creat a dictionary where the key value is the global ID and the value is the number of times it appears in a list
relates_Dict_C = Counter(relatesList)
relates_Dict = dict(relates_Dict_C)

#print relates_Dict


#Check how many relationships each parcel has then copy that parcel x number of times so it exists in the featureclass as many times as it has relationships
print "Creating one Parcel for each parcel relate"
with arcpy.da.SearchCursor(fc5, Fieldlist) as scur:
    with arcpy.da.InsertCursor(fc4, Fieldlist) as cursor:
        for row in scur:
            keyValue = str(row[30])

            if keyValue in relates_Dict:

                insertCounter = (relates_Dict[keyValue])-1

                if insertCounter == 0:

                    pass

                else:


                    for i in range(insertCounter):
                        print insertCounter
                        cursor.insertRow(row)
