#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      UKPXR011
#
# Created:     09/06/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os

workspace = 'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Senario_Update\AP_SG_20200616b\AP_SG_20200616.gdb'
desktopPath = 'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Senario_Update'
fc1 = 'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Senario_Update\HS2B_Safeguarding_2020_Leeds_20200616_135033\Output.gdb\Required_LOP'
fc2 = 'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Leeds_SOPS\Senario_Update\AP_SG_20200616b\AP_SG_20200616.gdb\STATUTORY_PROCESSES\Safeguarding_Land_Ownership_Parcels'
n = 9
n1=8
count = 0

# Get a list of fields from the InputLOP feature
UpdateFields = [f.name for f in arcpy.ListFields(fc1)]
#print UpdateFields
#Delete the first 9 from the list as they dont need updating
del UpdateFields[:n]
#Append back in to the list OwnershipReferenceNumber as it is needed to Join
UpdateFields.insert(0,"OwnershipReferenceNumber")


#Get a list of fields from SDE
CurrentFields = [f.name for f in arcpy.ListFields(fc2)]
#Delete the first 8 as they dont need to be updated
del CurrentFields[:n1]
#Append in the ownership reference number to the start of the list
CurrentFields.insert(0,"OwnershipReferenceNumber")



#Make A dictionary out of the required LOP plus update fields
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc1,UpdateFields)}


#Start Edditing
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

#Update cursor with the checkout and fields for updating
with arcpy.da.UpdateCursor(fc2, CurrentFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:


                updateRow[1]= valueDict[keyValue][0]
                updateRow[2]= valueDict[keyValue][1]
                updateRow[3]= valueDict[keyValue][2]
                updateRow[4]= valueDict[keyValue][3]
                updateRow[5]= valueDict[keyValue][4]
                updateRow[6]= valueDict[keyValue][5]
                updateRow[7]= valueDict[keyValue][6]
                updateRow[8]= valueDict[keyValue][7]
                updateRow[9]= valueDict[keyValue][8]
                updateRow[10]= valueDict[keyValue][9]
                updateRow[11]= valueDict[keyValue][10]
                updateRow[12]= valueDict[keyValue][11]
                updateRow[13]= valueDict[keyValue][12]
                updateRow[14]= valueDict[keyValue][13]
                updateRow[15]= valueDict[keyValue][14]
                updateRow[16]= valueDict[keyValue][15]
                updateRow[17]= valueDict[keyValue][16]
                updateRow[18]= valueDict[keyValue][17]
                updateRow[19]= valueDict[keyValue][18]
                updateRow[20]= valueDict[keyValue][19]
                updateRow[21]= valueDict[keyValue][20]
                updateRow[22]= valueDict[keyValue][21]
                updateRow[23]= valueDict[keyValue][22]
                updateRow[24]= valueDict[keyValue][23]
                updateRow[25]= valueDict[keyValue][24]
                updateRow[26]= valueDict[keyValue][25]
                updateRow[27]= valueDict[keyValue][26]
                updateRow[28]= valueDict[keyValue][27]
                updateRow[29]= valueDict[keyValue][28]
                updateRow[30]= valueDict[keyValue][29]
                updateRow[31]= valueDict[keyValue][30]
                updateRow[32]= valueDict[keyValue][31]
                updateRow[33]= valueDict[keyValue][32]
                updateRow[34]= valueDict[keyValue][33]
                updateRow[35]= valueDict[keyValue][34]
                updateRow[36]= valueDict[keyValue][35]
                updateRow[37]= valueDict[keyValue][36]
                updateRow[38]= valueDict[keyValue][37]
                updateRow[39]= valueDict[keyValue][38]
                updateRow[40]= valueDict[keyValue][39]
                updateRow[41]= valueDict[keyValue][40]
                updateRow[42]= valueDict[keyValue][41]
                updateRow[43]= valueDict[keyValue][42]
                updateRow[44]= valueDict[keyValue][43]
                updateRow[45]= valueDict[keyValue][44]
                updateRow[46]= valueDict[keyValue][45]
                updateRow[47]= valueDict[keyValue][46]
                updateRow[48]= valueDict[keyValue][47]
                updateRow[49]= valueDict[keyValue][48]
                updateRow[50]= valueDict[keyValue][49]
                updateRow[51]= valueDict[keyValue][50]
                updateRow[52]= valueDict[keyValue][51]
                updateRow[53]= valueDict[keyValue][52]
                updateRow[54]= valueDict[keyValue][53]
                updateRow[55]= valueDict[keyValue][54]
                updateRow[56]= valueDict[keyValue][55]
                updateRow[57]= valueDict[keyValue][56]
                updateRow[58]= valueDict[keyValue][57]
                updateRow[59]= valueDict[keyValue][58]
                updateRow[60]= valueDict[keyValue][59]
                updateRow[61]= valueDict[keyValue][60]
                updateRow[62]= valueDict[keyValue][61]
                updateRow[63]= valueDict[keyValue][62]
                updateRow[64]= valueDict[keyValue][63]
                updateRow[65]= valueDict[keyValue][64]
                updateRow[66]= valueDict[keyValue][65]
                updateRow[67]= valueDict[keyValue][66]
                updateRow[68]= valueDict[keyValue][67]
                updateRow[69]= valueDict[keyValue][68]
                updateRow[70]= valueDict[keyValue][69]
                updateRow[71] = valueDict[keyValue][71]
                updateRow[72] = valueDict[keyValue][72]
                updateRow[73] = valueDict[keyValue][73]
                updateRow[74] = valueDict[keyValue][74]
                updateRow[75] = valueDict[keyValue][75]
                updateRow[76] = valueDict[keyValue][76]
                updateRows.updateRow(updateRow)




edit.stopOperation()
edit.stopEditing(True)
