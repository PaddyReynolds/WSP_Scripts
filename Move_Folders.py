#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     16/10/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

import arcpy
import os
import shutil
from shutil import copyfile
import datetime

#set up veriables
scratch = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Script_Test\Scratch.gdb'
schema = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Script_Test\Schema\C863-MCL-GI-GDD-000-000509_XXX\Y20WXX.gdb'
xml= r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\Script_Test\Schema\C863-MCL-GI-GDD-000-000509_XXX\HS2-HS2-GI-SPE-000-000018_P07.xml'
version = 'P20'
x = datetime.datetime.now()
week =  x.isocalendar()[1]
Doc_Numb = 'C863-MCL-GI-GDD-000-000509'

#move folder to this weeks folder and set names etc.
weekly_Folder = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\C863-MCL-GI-GDD-000-000509_'+ str(version)
os.mkdir(weekly_Folder)

#Copy GDB to new folder
out_data = weekly_Folder + "\\" + 'Y20W'+str(week)+'.gdb'
arcpy.Copy_management(schema, out_data)

#Move XML
out_data = weekly_Folder + '\\HS2-HS2-GI-SPE-000-000018_P07.xml'
arcpy.Copy_management(xml, out_data)

#Inputs
fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\GDD_Extracts\Extract_22102020.gdb\STATUTORY_PROCESSES\LAA'
fc2 = r'C:\Users\UKPXR011\Desktop\Current Work\2A\GDD\GDD_Extracts\Extract_22102020.gdb\STATUTORY_PROCESSES\LandAcquisitionParcels'
fc3 = weekly_Folder + "\\" + 'Y20W'+str(week)+'.gdb'+'\\'+'PRP_MCL_C863_LandAcquisitionAreas_Ply'
fc4 = weekly_Folder + "\\" + 'Y20W'+str(week)+'.gdb'+'\\'+'PRP_MCL_C863_LandAcquisitionParcels_Ply'
fc5 = scratch +'\\' + 'LAA_Dissolve1'
fc6 = scratch +'\\' + 'LAA_Dissolve2'

#Delete scratch features
if arcpy.Exists(fc5):
    arcpy.Delete_management(fc5)
if arcpy.Exists(fc6):
    arcpy.Delete_management(fc6)

LapID = []

# Create a cursor of LAPS from extract and then insert them into to blank schema
#                 0             1               2                       3          4            5           6           7           8           9       10          11          12          13         14       15              16      17
#hs2_Fields =['HS2_AssetID','HS2_AssetName','HS2_SuitabilityCode','HS2_Phase','HS2_DocNum','HS2_DocRev','Contract','Originator','HS2_SupDoc','LAPID', 'LAPStatus', 'LAPDesc', 'NumOnPlan', 'LAAID', 'LAAName', 'LRType', 'NoticeType','@SHAPE']
hs2_Fields =['LAPID', 'LAPStatus', 'LAPDesc', 'LRType', 'NoticeType','SHAPE@']
#Append in old geometry for features
#                0      1           2           3       4           5
LAPFields = ['LAPID','LAPStatus','LAPDesc','LRType','NoticeType','SHAPE@']
with arcpy.da.SearchCursor(fc2,LAPFields) as searchRows:
    cursor = arcpy.da.InsertCursor(fc4, hs2_Fields)

    for row in searchRows:
        LapID.append(row[0])
        cursor.insertRow(row)
del cursor

#Start Edditing
edit = arcpy.da.Editor(weekly_Folder)
edit.startEditing(False, True)
edit.startOperation()

#Update the fields that have static attributes
#               0               1                   2                   3          4            5           6           7           8           9           10          11      12
hs2_Fields =['HS2_AssetID','HS2_AssetName','HS2_SuitabilityCode','HS2_Phase','HS2_DocNum','HS2_DocRev','Contract','Originator','HS2_SupDoc', 'NumOnPlan', 'LAAID', 'LAAName','LAPID']

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

                #LAAID
                updateRow[10] = 'N/A'

                #LAAName
                updateRow[11] = 'N/A'

                #LAPID
                updateRow[12] = 'LAP'+str(updateRow[12])


                updateRows.updateRow(updateRow)

edit.stopOperation()
edit.stopEditing(True)


#Copy information from LAA layer in extract and import it into empty featureclass
hs2_Fields =['LAAID','LAAName','LAAStatus','LRType','SHAPE@']

expression = """LAAStatus IN( 'DEL','WIP' )"""
#Append in old geometry for features
#                0      1           2           3       4           5
LAAFields = ['LAAID','LAAName','LAAStatus','LRType','SHAPE@']
with arcpy.da.SearchCursor(fc1,LAAFields, expression) as searchRows:
    cursor = arcpy.da.InsertCursor(fc3, hs2_Fields)

    for row in searchRows:
        cursor.insertRow(row)
del cursor


#Multipart to single part to count the number of features per LAA to work out whcih are multiparts
arcpy.MultipartToSinglepart_management(fc3, fc5)
arcpy.Dissolve_management(fc5, fc6,"LAAID", "LAAID COUNT")

Multipart_Fields = ['LAAID', 'COUNT_LAAID']


valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc6,Multipart_Fields)}

#Start Edditing
edit = arcpy.da.Editor(weekly_Folder)
edit.startEditing(False, True)
edit.startOperation()

#Update static fields
#              0                       1            2              3          4            5           6           7          8
hs2_Fields =['HS2_SuitabilityCode','HS2_Phase','HS2_DocNum','HS2_DocRev', 'Contract', 'Originator', 'Multipart', 'DescUse','LAAID']

with arcpy.da.UpdateCursor(fc3, hs2_Fields) as updateRows:

    for updateRow in updateRows:



                #work out multipart field by marking Yes when count is greater than 1
                keyValue = updateRow[8]
                if keyValue in valueDict:
                    if valueDict[keyValue][0] > 1 :
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

                updateRows.updateRow(updateRow)

edit.stopOperation()
edit.stopEditing(True)

#QC Feature Classes

fc7 =
fc8 =
fc9 =
fc10 =

#Delete scratch features
fcList = [fc7, fc8, fc9, fc10]
for fc in fcList:

    if arcpy.Exists(fc):
        arcpy.Delete_management(fc)



#Check for duplicate LAPIDS

LapSet = set([x for x in Lnumbers if Lnumbers.count(x) > 1])
#Check for Duplicate Lnumbers
if len(LapID) != 0:
    Errors.append("Duplicate Lnumbers")
    ErrorCount =ErrorCount + 1

#Check for Duplica LAA ids


#Check for duplicate LAA Names

#Check for multipart LAPS

#Check for geometry errors



