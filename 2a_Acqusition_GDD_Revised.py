#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     29/09/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
import shutil
import shutil
from shutil import copyfile
import datetime

#set up veriables
schema = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Schema\Y21WXX.gdb'
XML = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Schema\HS2-HS2-GI-SPE-000-000018_P08.xml'
version = 'C34'
x = datetime.datetime.now()
week =  x.isocalendar()[1]
Doc_Numb = 'C863-MCL-GI-GDD-A000-000002'


#move folder to this weeks folder and set names etc.

folder = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\C863-MCL-GI-GDD-A000-000002_'+ str(version)
scratchGDB = folder+"\\"+"Scratch.gdb"
if os.path.isdir(folder) is True:
    shutil.rmtree(folder)
    os.mkdir(folder)

else:
    os.mkdir(folder)

weekly_Folder = folder+'\\'+'Y22W'+str(week)+'.gdb'
arcpy.Copy_management(schema, weekly_Folder)
XMLdst = folder+"\\"+"HS2-HS2-GI-SPE-000-000018_P08.xml"
copyfile(XML, XMLdst)
arcpy.management.CreateFileGDB(folder, "Scratch")


#Inputs
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Extract\31032022.gdb\LAA'
fc2 = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Extract\31032022.gdb\LAPS'
desc= arcpy.Describe(fc2)
gdb = desc.path
fc3 = weekly_Folder+'\\PRP_MCL_C863_LandAcquisitionAreas_Ply'
fc4 = weekly_Folder+ '\\PRP_MCL_C863_LandAcquisitionParcels_Ply'
fc5 = scratchGDB +'\\' + 'LAA_Dissolve1'
fc6 = scratchGDB +'\\' + 'LAA_Dissolve2'


sourceFC = r"C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Extract\23122021.gdb\Fixes"

sourceFieldsList = ["LAPID", "LAAID", "LAPStatus"]

# Use list comprehension to build a dictionary from a da SearchCursor where the key values are based on 3 separate feilds
valueDict = {str(r[0]) + "," + str(r[1]):(r[2:]) for r in arcpy.da.SearchCursor(sourceFC, sourceFieldsList)}

#edit = arcpy.da.Editor(gdb)
#edit.startEditing(False, True)
#edit.startOperation()
updateFieldsList = ["LAPID", "LAAID", "LAPStatus"]

with arcpy.da.UpdateCursor(fc2, updateFieldsList) as updateRows:
    for updateRow in updateRows:
        # store the Join value by combining 3 field values of the row being updated in a keyValue variable
        keyValue = updateRow[0]+ "," + str(updateRow[1])
        # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[2] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

del valueDict

#edit.stopOperation()
#edit.stopEditing(True)

TidyFields = ['LAAID','LAPType','LAPDesc']
with arcpy.da.UpdateCursor(fc2, TidyFields) as updateRows:
    for updateRow in updateRows:
        LAA = str(updateRow[0])
        if LAA.startswith('A'):
                updateRow[1] = 'NOT'

        else:
            updateRow[0] = 'N/A'
            updateRow[1] = 'BAS'

        if updateRow[2] is None:
            updateRow[2] = 'N/A'


        updateRows.updateRow(updateRow)
#                0             1               2                       3          4            5           6           7           8           9       10          11          12          13         14       15              16      17
#hs2_Fields =['HS2_AssetID','HS2_AssetName','HS2_SuitabilityCode','HS2_Phase','HS2_DocNum','HS2_DocRev','Contract','Originator','HS2_SupDoc','LAPID', 'LAPStatus', 'LAPDesc', 'NumOnPlan', 'LAAID', 'LAAName', 'LRType', 'NoticeType','@SHAPE']
hs2_Fields =['LAPID','LAPStatus','LAPDesc','LAAID','LRType','NoticeType','LAPType','SHAPE@']
#Append in old geometry for features
#                0      1           2           3       4           5       6
LAPFields = ['LAPID','LAPStatus','LAPDesc','LAAID','LRType','NoticeType','LAPType','SHAPE@']
with arcpy.da.SearchCursor(fc2,LAPFields) as searchRows:
    cursor = arcpy.da.InsertCursor(fc4, hs2_Fields)

    for row in searchRows:
        cursor.insertRow(row)
del cursor

#Start Edditing
edit = arcpy.da.Editor(weekly_Folder)
edit.startEditing(False, True)
edit.startOperation()

#               0               1                   2                   3          4            5           6           7           8           9            10     11        12
hs2_Fields =['HS2_AssetID','HS2_AssetName','HS2_SuitabilityCode','HS2_Phase','HS2_DocNum','HS2_DocRev','Contract','Originator','HS2_SupDoc', 'NumOnPlan' ,'CRID','LAPType','LAPID']

with arcpy.da.UpdateCursor(fc4, hs2_Fields) as updateRows:

    for updateRow in updateRows:
                #HS2_SuitabilityCode
                updateRow[2] = 'SC2'

                #HS2_Phase
                updateRow[3] = 'R3'

                #HS2_DocNum
                updateRow[4] = Doc_Numb

                #HS2_DocRev
                updateRow[5] = version

                #Contract
                updateRow[6] = 'C863'

                #Originator
                updateRow[7] = 'MCL'

                #NumOnPlan

                updateRow[9] = 'N/A'

                #CRID
                updateRow[10] = 'N/A'

                #Notice Type

                updateRows.updateRow(updateRow)

edit.stopOperation()
edit.stopEditing(True)


hs2_Fields =['LAAID','LAAName','LAAStatus','LRType','SHAPE@']

#Append in old geometry for features
#                0      1           2           3       4           5
LAAFields = ['LAAID','LAAName','LAAStatus','LRType','SHAPE@']
with arcpy.da.SearchCursor(fc1,LAAFields) as searchRows:
    cursor = arcpy.da.InsertCursor(fc3, hs2_Fields)

    for row in searchRows:
        cursor.insertRow(row)
del cursor


#Start Edditing
edit = arcpy.da.Editor(weekly_Folder)
edit.startEditing(False, True)
edit.startOperation()

#               0                       1            2              3          4            5           6           7          8     9        10
hs2_Fields =['HS2_SuitabilityCode','HS2_Phase','HS2_DocNum','HS2_DocRev', 'Contract', 'Originator', 'Multipart', 'DescUse','LAAID','CRID','SHAPE@']

with arcpy.da.UpdateCursor(fc3, hs2_Fields) as updateRows:

    for updateRow in updateRows:


                if updateRow[10].isMultipart is True:
                    updateRow[6] = 'Y'

                else:
                    updateRow[6] = 'N'
                #HS2_SuitabilityCode
                updateRow[0] = 'SC2'

                #HS2_Phase
                updateRow[1] = 'R3'

                #HS2_DocNum
                updateRow[2] = Doc_Numb

                #HS2_DocRev
                updateRow[3] = version

                #Contract
                updateRow[4] = 'C863'

                #Originator
                updateRow[5] = 'MCL'

                updateRow[7] = 'N/A'

                updateRow[9] = 'N/A'

                updateRows.updateRow(updateRow)


#make dictionary of LAAID and CLR

CLR_Fields = ['LAAID', 'LAAName']

valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc3,CLR_Fields)}

#update cursor LAP

with arcpy.da.UpdateCursor(fc4, CLR_Fields) as updateRows:

    for updateRow in updateRows:

                keyValue = updateRow[0]

                if keyValue in valueDict:
                    updateRow[1] = valueDict[keyValue][0]

                else:
                    updateRow[1] = "N/A"

                updateRows.updateRow(updateRow)



edit.stopOperation()
edit.stopEditing(True)





