#-------------------------------------------------------------------------------
# Name:        Update Relate Table Script
# Purpose:     Automate relating two layers on GIS
#
# Author:      UKKXR602
#
# Created:     07/10/2019
# Copyright:   (c) UKKXR602 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
import shutil
import datetime

#Date
now = datetime.datetime.now()
Date = now.strftime("%Y%m%d%H%M")

#Create work space
desktopPath = os.environ.get( "USERPROFILE" ) + "\\Desktop"
os.makedirs(desktopPath + "\\Hs2_Amend_relates_table_" + str(Date))
TempFolder = desktopPath + "\\Hs2_Amend_relates_table_" + str(Date)
WorkFolder = TempFolder
GDB = "Relates_Amend_Update"
WorkGDD = WorkFolder + "\\" + GDB + ".gdb"
arcpy.CreateFileGDB_management(TempFolder,GDB)
arcpy.env.workspace = WorkGDD

#variables for input table
relationship_tab = arcpy.GetParameterAsText(0)
origin_field = arcpy.GetParameterAsText(1)
destination_Field = arcpy.GetParameterAsText(2)

#Get Origin and Destination FC Names
desc = arcpy.Describe(relationship_tab)
origin_path = str(desc.path)
origin_FC = str(desc.backwardPathLabel)
destin_FC = str(desc.forwardPathLabel)
origin_FC_Name = origin_path + "\\" + origin_FC
destination_FC_Name = origin_path + "\\" + destin_FC
origin_Featureclass = origin_FC_Name
destination_Featureclass = destination_FC_Name

#add values to store
temp_origin_field = "OriginGlobalID"
temp_destin_field = "DestGlobalID"
temp_origin_area = 'Origi_Area'
temp_destin_area = 'Dest_Area'
temp_origin_perc = 'Origin_Perc'
temp_destin_perc = 'Dest_Perc'

#variables for updating the relates table
dissFC = "Dissolve_Analysis"
intFC = "Inter_Analysis"
GlobalID = "GlobalID"
inputs = "SHAPE@AREA"

#relates tables to input into
desc1 = arcpy.Describe(origin_Featureclass)
desc2 = arcpy.Describe(destination_Featureclass)

PrimaryName = "FID_" + str(desc1.name)
SecondName = "FID_" + str(desc2.name)

#OverlapValue Paramaters
overlap_sq_M = 'Overlap_SqM'
overlap_perc = 'Overlap1_Per'
overlap_perc2 = 'Overlap2_Per'

#clear_current_table
arcpy.TruncateTable_management(relationship_tab)

#Intersect/dissolve two fields to be compared then populate relates table
#with globalIDs and get overlap areas
arcpy.Intersect_analysis([origin_Featureclass,destination_Featureclass],intFC,"ALL","","INPUT")
arcpy.Dissolve_management(intFC,dissFC,[PrimaryName,SecondName])
#arcpy.RepairGeometry_management(dissFC)
arcpy.AddField_management(dissFC,temp_origin_field, "GUID", "", "", "", "", "NULLABLE")
arcpy.AddField_management(dissFC,temp_destin_field, "GUID", "", "", "", "", "NULLABLE")
arcpy.AddField_management(dissFC,temp_origin_area,"DOUBLE","","","","","NULLABLE")
arcpy.AddField_management(dissFC,temp_destin_area,"DOUBLE","","","","","NULLABLE")
arcpy.AddField_management(dissFC,temp_origin_perc,"DOUBLE","","","","","NULLABLE")
arcpy.AddField_management(dissFC,temp_destin_perc,"DOUBLE","","","","","NULLABLE")

#create list of GloablIDs to put into dissolve and link them do data using input origin field (acts as a join)
origin_valDict = {r[0]:(r[1:])for r in arcpy.da.SearchCursor(origin_Featureclass,["OBJECTID",GlobalID])}
with arcpy.da.UpdateCursor(dissFC,[PrimaryName,temp_origin_field]) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in origin_valDict:
            updateRow[1] = origin_valDict[keyValue][0]
            updateRows.updateRow(updateRow)

del origin_valDict
#create list for destination GlobIDs to link them to do using input of destinationfeature class
dest_valDict = {r[0]:(r[1:])for r in arcpy.da.SearchCursor(destination_Featureclass,["OBJECTID",GlobalID])}
with arcpy.da.UpdateCursor(dissFC,[SecondName,temp_destin_field]) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in dest_valDict:
            updateRow[1] = dest_valDict[keyValue][0]
            updateRows.updateRow(updateRow)

del dest_valDict
#create list for origin global ID to pull across original areas for percent comparison
ori_area_valDict =  {r[0]:(r[1:])for r in arcpy.da.SearchCursor(origin_Featureclass,["OBJECTID",inputs])}
with arcpy.da.UpdateCursor(dissFC,[PrimaryName,temp_origin_area]) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in ori_area_valDict:
            updateRow[1] = ori_area_valDict[keyValue][0]
            updateRows.updateRow(updateRow)

del ori_area_valDict
#Create a list for destination feature to pull across areas for destination feature for percent  comparison
dest_area_valDict = {r[0]:(r[1:])for r in arcpy.da.SearchCursor(destination_Featureclass,["OBJECTID",inputs])}
with arcpy.da.UpdateCursor(dissFC,[SecondName,temp_destin_area]) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in dest_area_valDict:
            updateRow[1] = dest_area_valDict[keyValue][0]
            updateRows.updateRow(updateRow)

del dest_area_valDict
#cross reference area of dissolve against original area and calculate percentage covered
#there can be slight discrepencies when intersecting and dissolving so if dissolve area is slightly large
#the script will just auto set it to 100% instead of say 100.003%
with arcpy.da.UpdateCursor(dissFC,["Origi_Area","Dest_Area","SHAPE@AREA","Origin_Perc",]) as cursor:
    for row in cursor:
        if row[2] >= row[0]:
            row[3] = 100
        else:
            row[3] = (row[2] * 100) / row[0]
        cursor.updateRow(row)
#repeat previous step but for comparing how much of the destination layer is covered by the original
with arcpy.da.UpdateCursor(dissFC,["Dest_Area","SHAPE@AREA","Dest_Perc",]) as descursor:
    for row in descursor:
        if row[1] >= row[0]:
            row[2] = 100
        else:
            row[2] = (row[1] * 100) / row[0]
        descursor.updateRow(row)

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "Dissolve_Analyisis"

diss_data_fields = ['SHAPE_Area',temp_origin_field,temp_destin_field,temp_origin_perc,temp_destin_perc]
relate_import_fields = ['Overlap_SqM',origin_field,destination_Field,overlap_perc,overlap_perc2]

with arcpy.da.SearchCursor(dissFC,diss_data_fields) as scur:
    with arcpy.da.InsertCursor(relationship_tab,relate_import_fields) as icur:
        for row in scur:
            icur.insertRow(row)