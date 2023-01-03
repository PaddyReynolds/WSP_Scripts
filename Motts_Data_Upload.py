#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     22/03/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import datetime
#Motts Data Transfer Script

now = datetime.date.today()
dateFormatted = (now.strftime("%d/%m/%Y"))

print dateFormatted
Last_Upload = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Motts\Motts_Data_Delivery_07042021\Motts_Data_Delivery_07042021.gdb'
New_Upload = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Motts\Motts_Data_Delivery_Final\Delivery\Motts_Data_Delivery_Final.gdb'


fc1 = Last_Upload + "\STATUTORY_PROCESSES\LandOwnershipParcels"
fc2 = Last_Upload + "\STATUTORY_PROCESSES\LAA"
fc3 = Last_Upload + "\STATUTORY_PROCESSES\LandAcquisitionParcels"

fc4 = New_Upload + "\STATUTORY_PROCESSES\LandOwnershipParcels"
fc5 = New_Upload + "\STATUTORY_PROCESSES\LAA"
fc6 = New_Upload + "\STATUTORY_PROCESSES\LandAcquisitionParcels"

NewFcs = [fc4,fc5,fc6]
OldFcs = [fc1,fc2,fc3]


for i in NewFcs:
    arcpy.AddField_management(i,'Geometry_Change','DATE')

#Start Edditing
edit = arcpy.da.Editor(New_Upload)
edit.startEditing(False, True)
edit.startOperation()


for i in range(3):

    updateFields = ['GlobalID','Geometry_Change','SHAPE@']
    OldFC = OldFcs[i]
    NewFC = NewFcs[i]
    valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(OldFC,updateFields)}
    with arcpy.da.UpdateCursor(NewFC, updateFields) as updateRows:
        for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
            keyValue = updateRow[0]
            # verify that the keyValue
            if keyValue in valueDict:
                updateRow[1] = valueDict[keyValue][0]
                if updateRow[2] <> valueDict[keyValue][1]:
                    updateRow[1] = dateFormatted
            updateRows.updateRow(updateRow)

    print str(NewFC + " Complete")


edit.stopOperation()
edit.stopEditing(True)

print "Not a Chance That Worked"











