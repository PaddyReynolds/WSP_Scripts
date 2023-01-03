#-------------------------------------------------------------------------------
# Name:        LAA LAP Relate script
# Purpose:     Script compares LAA to Lap relationships
#
# Author:      UKKXR602
#
#Hi Mate,
#The relate script V1 im thinking should do something basic like this:
#1.	Check every LAP has a LOP relate
#2.	LAA’s that aren’t in progress have their lap relates cleared
#3.	Check that Survey LAPS aren’t Related to Posession LAA’s and the other way around
#4.	Check that if a LAP has a LAA assigned to it in the LAAID field within the laps that it is related to that LAA
#I started this months ago and then got distracted but I basically got nowhere with it.
#It would be really useful to have though and then could build it into a QC check thingy every day or run it on a checkout and correct then check back in,

#Let me know what you think


# Created:     04/03/2021
# Copyright:   (c) UKKXR602 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
import shutil
import datetime

#start time
startTime = datetime.datetime.now()
#Date
now = datetime.datetime.now()
Date = now.strftime("%Y%m%d%H%M%S")
Date2 = now.strftime("%Y%m%d")
Date3 = now.strftime("%d/%m/%Y")

#Create workspace
TempFolder = r'C:\Users\UKPXR011\Desktop\Scripts\Relate_Checker'
WorkFolder = TempFolder
GDB = "WORKGDD"
WorkGDD = WorkFolder + "\\" + GDB + ".gdb"
arcpy.CreateFileGDB_management(TempFolder,GDB)
arcpy.env.workspace = WorkGDD


#InputGDD
input_GDD = r'C:\Users\UKPXR011\Desktop\Scripts\Relate_Checker\Test_GDB.gdb'

#Features to check
LAP = input_GDD + "\\" + 'STATUTORY_PROCESSES' + "\\" + 'LandAcquisitionParcels'
LAA = input_GDD + "\\" + 'STATUTORY_PROCESSES' + "\\" + 'LAA'
LOP = input_GDD + "\\" + 'STATUTORY_PROCESSES' + "\\" + 'LandOwnershipParcels'
LAP_LOP_Rel = input_GDD + "\\" + 'STATUTORY_PROCESSES' + "\\" + 'relLAPs_LandOwnership'
LAA_LAP_Rel = input_GDD + "\\" + 'STATUTORY_PROCESSES' + "\\" + 'relLAA_LAPs'

#Key fields within features
LAP_ID = 'LAPID'
GlobID = 'GlobalID'
LAP_GUID = 'LAPsGlobalID'
LAA_Progres_Query = "LAAStatus IN( 'SUP' , 'DEL' ) OR LAAStatus IS NULL"
LAP_ACCESS_Compare_Query = ""
LAA_ACCESS_Compare_Query = ""

#Scrap Features
LAP_LOP_Table = 'Lap_LOP_Table'
LAP_ACCESS_Table = 'LAP_Access_Table'
LAP_LAA_Access_Compare = 'LAP_LAA_Access'
LAP_LOP_Table_Use = WorkGDD + "\\" + LAP_LOP_Table
#Make List of LandownershipParcels and LAP to check all are related
LAP_List = []

#Testing which LAPs have a relate
arcpy.CreateTable_management(WorkGDD,LAP_LOP_Table)
arcpy.AddField_management(LAP_LOP_Table_Use,'GUID','TEXT','','100')
arcpy.AddField_management(LAP_LOP_Table_Use,'LAPID','TEXT','','8')
arcpy.AddField_management(LAP_LOP_Table_Use,'Has_Rel','TEXT','','5')

#Create table to test LAP / LAA Access
arcpy.CreateTable_management(WorkGDD,LAP_ACCESS_Table)
arcpy.AddField_management(LAP_ACCESS_Table,'GUID_LAA','TEXT','','','100')
arcpy.AddField_management(LAP_ACCESS_Table,'GUID_LAP','TEXT','','','100')
arcpy.AddField_management(LAP_ACCESS_Table,'GUID_rel','TEXT','','','100')
arcpy.AddField_management(LAP_ACCESS_Table,'LAAID','TEXT','','','30')
arcpy.AddField_management(LAP_ACCESS_Table,'LAPID','TEXT','','','8')
arcpy.AddField_management(LAP_ACCESS_Table,'LR_Type_LAA','TEXT','','','5')
arcpy.AddField_management(LAP_ACCESS_Table,'LR_Type_LAPID','TEXT','','','5')
arcpy.AddField_management(LAP_ACCESS_Table,'Match','TEXT','','','10')
arcpy.AddField_management(LAP_ACCESS_Table,'LAP_LAAID','TEXT','','','30')
arcpy.AddField_management(LAP_ACCESS_Table,'LAAID_Match','TEXT','','','10')

#Create table for checkign LAAID between LAPS and LAA

arcpy.AddMessage("Generating Table of LAPS / against GUI")
#Get GlobID and LAPID and put into table to compare against relates - use
#Global ID in case there are duplicate LAPID
LAP_Search = [[L[0],L[1]] for L in arcpy.da.SearchCursor(LAP,[GlobID,LAP_ID,])]
LAA_LOP_ins = arcpy.da.InsertCursor(LAP_LOP_Table_Use,['GUID','LAPID'])
for row in LAP_Search:
    LAA_LOP_ins.insertRow(row)

#Check through relationship table and make list of GUIDs then compare
#against LAP list to see which ones are missing a relate
with arcpy.da.SearchCursor(LAP_LOP_Rel,LAP_GUID) as cursor:
    for row in cursor:
        LAP_List.append(row[0])

del cursor
del LAA_LOP_ins
del LAP_Search

MissingLOP_LAP_count = 0
LAP_missingLOP = []

with arcpy.da.UpdateCursor(LAP_LOP_Table_Use,['GUID','LAPID','HAS_Rel']) as cursor:
    for row in cursor:
        if row[0] in LAP_List:
            row[2] = 'Yes'
            cursor.updateRow(row)
        else:
            MissingLOP_LAP_count+=1
            row[2] = 'No'
            LAP_missingLOP.append(row[1])
            cursor.updateRow(row)

arcpy.AddMessage(str(MissingLOP_LAP_count) + " LAPs without a parcel relate")

if MissingLOP_LAP_count > 0:
    with open(os.path.join(WorkFolder,"LAPS_missing_LOP.csv"), "w") as f:
        for item in LAP_missingLOP:
            f.write("%s\n" % item)

del cursor

#GUID for LAA that are not in progress
LAA_Non_Progress = []
LAAID_Not_In_Progress = []
LAAID_Not_Progres_Clean = list(dict.fromkeys(LAAID_Not_In_Progress))
LAA_Not_Progress_count = 0

#Search LAA feature to get GlobalID of relevent LAA that aren't in progress
with arcpy.da.SearchCursor(LAA,['GlobalID','LAAID'],LAA_Progres_Query) as cursor:
    for row in cursor:
        LAA_Not_Progress_count+=1
        LAA_Non_Progress.append(str(row[0]))
        LAAID_Not_In_Progress.append(str(row[1]))

arcpy.AddMessage(str(LAA_Not_Progress_count) + " - LAA not in progress")
del row
del cursor

#Create text document of all the LAA relates that are going to be removed
if LAA_Not_Progress_count > 0:
    with open(os.path.join(WorkFolder,"LAA_Not_In_Progress_unRelated.csv"), "w") as f:
        for item in LAAID_Not_In_Progress:
            f.write("%s\n" % item)
else:
    arcpy.AddMessage("No LAA relates removed")

#Remove the relates from the LAA / LAP relates
with arcpy.da.UpdateCursor(LAA_LAP_Rel,'LAAGlobalID') as cursor:
    for row in cursor:
        if row[0] in LAA_Non_Progress:
            cursor.deleteRow()

#Add LAA / LAP relates to new table so LR Types can be prepared
with arcpy.da.SearchCursor(LAA_LAP_Rel,['LAAGlobalID','LAPsGlobalID','GlobalID']) as scur:
    with arcpy.da.InsertCursor(LAP_ACCESS_Table,['GUID_LAA','GUID_LAP','GUID_rel']) as icur:
        for row in scur:
            icur.insertRow(row)

#fields to be transferred from LAA to table
LAA_sourceFields = ['GlobalID','LAAID','LRType']
LAA_updateFields = ['GUID_LAA','LAAID','LR_Type_LAA']

LAA_valDict = {r[0]:(r[1:])for r in arcpy.da.SearchCursor(LAA,LAA_sourceFields)}
with arcpy.da.UpdateCursor(LAP_ACCESS_Table,LAA_updateFields) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in LAA_valDict:
            for n in range (1,len(LAA_sourceFields)):
                updateRow[n] = LAA_valDict[keyValue][n-1]
            updateRows.updateRow(updateRow)
del updateRows
del LAA_valDict

#fields to be transferred from LAP to table
LAP_sourceFields = ['GlobalID','LAPID','LRType','LAAID']
LAP_updateFields = ['GUID_LAP','LAPID','LR_Type_LAPID','LAP_LAAID']

LAP_valDict = {r[0]:(r[1:])for r in arcpy.da.SearchCursor(LAP,LAP_sourceFields)}
with arcpy.da.UpdateCursor(LAP_ACCESS_Table,LAP_updateFields) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in LAP_valDict:
            for n in range (1,len(LAP_sourceFields)):
                updateRow[n] = LAP_valDict[keyValue][n-1]
            updateRows.updateRow(updateRow)
del updateRows
del LAP_valDict

arcpy.TableSelect_analysis(LAP_ACCESS_Table,LAP_LAA_Access_Compare, "LR_Type_LAA = 'ACCES' OR LR_Type_LAPID = 'ACCES'")

with arcpy.da.UpdateCursor(LAP_LAA_Access_Compare,['LR_Type_LAA','LR_Type_LAPID','Match']) as cursor:
    for row in cursor:
        if row[0] == row[1]:
            row[2] = 'Yes'

        else:
            row[2] = 'No'
        cursor.updateRow(row)

LAP_LAA_Count = 0
LAP_LAA_Remove_List = []
GUID_LAA_LAP_Access_remove = []
with arcpy.da.SearchCursor(LAP_LAA_Access_Compare,['LR_Type_LAA','LR_Type_LAPID','Match','GUID_rel','LAAID','LAPID'],"Match = 'No'") as cursor:
    for row in cursor:
        input_Lap_LAA = (str(row[4]) + " - " + str(row[5]) + " - " + str(row[0]) + " - " + str(row[1]))
        LAP_LAA_Remove_List.append(input_Lap_LAA)
        LAP_LAA_Count+=1
        GUID_LAA_LAP_Access_remove.append(str(row[3]))

arcpy.AddMessage(str(LAP_LAA_Count) + ' - LAP / LAA non-compliant access relates removed')

del row
del cursor

#Create text document of all the LAA relates that are going to be removed
if LAP_LAA_Count > 0:
    with open(os.path.join(WorkFolder,"LAA_LAA_Not_Both_Access.csv"), "w") as f:
        for item in LAP_LAA_Remove_List:
            f.write("%s\n" % item)
else:
    arcpy.AddMessage("No LAA / LAP Access relates removed")

#Remove the relates from the LAA / LAP relates where not agreed
with arcpy.da.UpdateCursor(LAA_LAP_Rel,'GlobalID') as cursor:
    for row in cursor:
        if row[0] in GUID_LAA_LAP_Access_remove:
            cursor.deleteRow()

del row
del cursor

#FLag where LAAID don't match between LAP and LAA
LAP_LAA_Match_count = 0
GUID_LAA_LAP_LAAID_Check = []
with arcpy.da.UpdateCursor(LAP_ACCESS_Table,['LAAID','LAP_LAAID','LAAID_Match','GUID_LAA','GUID_LAP'],"NOT LAP_LAAID = 'N/A'") as cursor:
    for row in cursor:
        if row[0] == row[1]:
            row[2] = 'Yes'

        else:
            row[2] = 'No'
            GUIs_LAA_LAP = 'LAA GUID is ' + str(row[3]) + ", LAP GUID IS " + str(row[4])
            GUID_LAA_LAP_LAAID_Check.append(GUIs_LAA_LAP)
            LAP_LAA_Match_count+=1
        cursor.updateRow(row)

del row
del cursor
arcpy.AddMessage(str(LAP_LAA_Match_count) + ' - LAA and LAP related with no match LAAID')

#Create text document of all LAA and LAP related with no match LAAID
if LAP_LAA_Match_count > 0:
    with open(os.path.join(WorkFolder,"LAA_LAA_Non_Matching_LAAID.csv"), "w") as f:
        for item in GUID_LAA_LAP_LAAID_Check:
            f.write("%s\n" % item)
else:
    arcpy.AddMessage("No LAA / LAP Access relates removed")


arcpy.AddMessage(datetime.datetime.now() - startTime)



