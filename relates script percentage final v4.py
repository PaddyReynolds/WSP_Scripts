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
relationship_tab = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\Manchester_SOPs\Manchester_Slops_3rd_Run\SLOP_SDE_Update.gdb\STATUTORY_PROCESSES\relSLOP_HMLR'
Sq_Metre_To_Disregard = 2
#Get Origin and Destination FC Names
arcpy.AddMessage("Getting origin/destination fields and feature classes")
desc = arcpy.Describe(relationship_tab)
origin_path = str(desc.path)
origin_FC = str(desc.backwardPathLabel)
destin_FC = str(desc.forwardPathLabel)
origin_FC_Name = origin_path + "\\" + origin_FC
destination_FC_Name = origin_path + "\\" + destin_FC
origin_Featureclass = origin_FC_Name
destination_Featureclass = destination_FC_Name

arcpy.AddMessage("The origin feature class is: " +str(origin_FC))
arcpy.AddMessage("The destination feature class is: " + str(destin_FC))

#Use describe to pull the origin and destination field names
origin_names = desc.originClassKeys
destination_names = desc.destinationClassKeys
dest_primary_group = destination_names[0]
dest_foreign_group = destination_names[1]
dest_primary = dest_primary_group[0]
dest_foreign = dest_foreign_group[0]
origin_primary_group = origin_names[0]
origin_foreign_group = origin_names[1]
origin_primary = origin_primary_group[0]
origin_foreign = origin_foreign_group[0]

arcpy.AddMessage("Origin primary field: " + str(origin_primary))
arcpy.AddMessage("Origin foreign field: " + str(origin_foreign))
arcpy.AddMessage("Destination primary field: " + str(dest_primary))
arcpy.AddMessage("Destination foreign field: " + str(dest_foreign))


#Calculate what type of field needs to be added for the original field based on
#in put original FC
origin_fields = arcpy.ListFields(origin_Featureclass)
field_type_list = []
field_type = str(field_type_list)

for field in origin_fields:
    field_name = field.name
    field_type = str(field.type)
    if field_name == origin_primary:
        field_type_list.append(field_type)

for typef in field_type_list:
    if typef == 'GlobalID':
        add_type = 'GUID'
    if typef == "String":
        add_type = "TEXT"
    if typef == "Integer":
        add_type = "LONG"
    if typef == 'OID':
        add_type = "LONG"

#Calculate what type of field needs to be added for the destination field based
#on input destionation FC
destin_fields = arcpy.ListFields(origin_Featureclass)
destin_field_type_list = []
destin_field_type = str(field_type_list)

for field in destin_fields:
    field_name = field.name
    field_type = str(field.type)
    if field_name == dest_primary:
        destin_field_type_list.append(field_type)

for typed in destin_field_type_list:
    if typed == 'GlobalID':
        add_type2 = 'GUID'
    if typed == "String":
        add_type2 = "TEXT"
    if typed == "Integer":
        add_type2 = "LONG"
    if typed == 'OID':
        add_type2 = "LONG"

arcpy.AddMessage("The origin field type is " + str(add_type))
arcpy.AddMessage("The destination field type is " + str(add_type2))

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
Origin_Foreign = str(dest_primary)
Destin_Foreign = str()
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

#Intersect/dissolve two fields to be compared then populate relates table
#with globalIDs and get overlap areas
arcpy.AddMessage("Use intersect/dissolve to build table of spatial intersections")
arcpy.Intersect_analysis([origin_Featureclass,destination_Featureclass],intFC,"ALL","","INPUT")
arcpy.Dissolve_management(intFC,dissFC,[PrimaryName,SecondName])
arcpy.RepairGeometry_management(dissFC)
arcpy.AddField_management(dissFC,temp_origin_field, add_type, "", "", "", "", "NULLABLE")
arcpy.AddField_management(dissFC,temp_destin_field, add_type2, "", "", "", "", "NULLABLE")
arcpy.AddField_management(dissFC,temp_origin_area,"DOUBLE","","","","","NULLABLE")
arcpy.AddField_management(dissFC,temp_destin_area,"DOUBLE","","","","","NULLABLE")
arcpy.AddField_management(dissFC,temp_origin_perc,"DOUBLE","","","","","NULLABLE")
arcpy.AddField_management(dissFC,temp_destin_perc,"DOUBLE","","","","","NULLABLE")

#clear_current_table
path = os.path.dirname(relationship_tab)
workspace = os.path.dirname(path)
arcpy.AddMessage(workspace)
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

relates_count =int(arcpy.GetCount_management(relationship_tab).getOutput(0))

if relates_count == 0:
    arcpy.AddMessage("Table doesn't have any relates in it")
else:
    arcpy.AddMessage("Clearing Table of existing relates")
    arcpy.TruncateTable_management(relationship_tab)
    arcpy.AddMessage("Relates table cleared")

#create list of GloablIDs to put into dissolve and link them do data using input origin field (acts as a join)
origin_valDict = {r[0]:(r[1:])for r in arcpy.da.SearchCursor(origin_Featureclass,["OBJECTID",origin_primary])}
with arcpy.da.UpdateCursor(dissFC,[PrimaryName,temp_origin_field]) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in origin_valDict:
            updateRow[1] = origin_valDict[keyValue][0]
            updateRows.updateRow(updateRow)

del origin_valDict
del(updateRow)
del(updateRows)
#create list for destination GlobIDs to link them to do using input of destinationfeature class
dest_valDict = {r[0]:(r[1:])for r in arcpy.da.SearchCursor(destination_Featureclass,["OBJECTID",dest_primary])}
with arcpy.da.UpdateCursor(dissFC,[SecondName,temp_destin_field]) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in dest_valDict:
            updateRow[1] = dest_valDict[keyValue][0]
            updateRows.updateRow(updateRow)

del dest_valDict
del(updateRow)
del(updateRows)
#create list for origin global ID to pull across original areas for percent comparison
ori_area_valDict =  {r[0]:(r[1:])for r in arcpy.da.SearchCursor(origin_Featureclass,["OBJECTID",inputs])}
with arcpy.da.UpdateCursor(dissFC,[PrimaryName,temp_origin_area]) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in ori_area_valDict:
            updateRow[1] = ori_area_valDict[keyValue][0]
            updateRows.updateRow(updateRow)

del ori_area_valDict
del(updateRow)
del(updateRows)
#Create a list for destination feature to pull across areas for destination feature for percent  comparison
dest_area_valDict = {r[0]:(r[1:])for r in arcpy.da.SearchCursor(destination_Featureclass,["OBJECTID",inputs])}
with arcpy.da.UpdateCursor(dissFC,[SecondName,temp_destin_area]) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in dest_area_valDict:
            updateRow[1] = dest_area_valDict[keyValue][0]
            updateRows.updateRow(updateRow)

del dest_area_valDict
del(updateRow)
del(updateRows)

#cross reference area of dissolve against original area and calculate percentage covered
#there can be slight discrepencies when intersecting and dissolving so if dissolve area is slightly large
#the script will just auto set it to 100% instead of say 100.003%
try:
    with arcpy.da.UpdateCursor(dissFC,["Origi_Area","Dest_Area","SHAPE@AREA","Origin_Perc",]) as cursor:
        for row in cursor:
            if row[2] >= row[0]:
                row[3] = 100
            else:
                row[3] = (row[2] * 100) / row[0]
            cursor.updateRow(row)
except:
    arcpy.AddMessage("Error Calcuating origin percentage field")

del(row)
del(cursor)
#repeat previous step but for comparing how much of the destination layer is covered by the original
try:
    with arcpy.da.UpdateCursor(dissFC,["Dest_Area","SHAPE@AREA","Dest_Perc",]) as descursor:
        for row in descursor:
            if row[1] >= row[0]:
                row[2] = 100
            else:
                row[2] = (row[1] * 100) / row[0]
            descursor.updateRow(row)
except:
    arcpy.AddMessage("Error Calcuating destination percentage field")

del(row)
del(descursor)

#Check to see if there is an Overlap_SqM field and if so remove any relates under the specified
#square metre to disregard (Sq_Metre_To_Disregard) or parameter #2
arcpy.AddMessage("Getting rid of relationships under " + str(Sq_Metre_To_Disregard) + " sq mtr")
check_overlap = arcpy.ListFields(relationship_tab)
overlap_list = []
for fid in check_overlap:
    overlap_list.append(fid.name)

delete_count = 0

for listed in overlap_list:
    if listed == 'Overlap_SqM':
        arcpy.AddMessage("Removing square metres too small from relates")
        with arcpy.da.UpdateCursor(relationship_tab,'Overlap_SqM') as delcursor:
            for row in delcursor:
                if int(row[1]) <= int(Sq_Metre_To_Disregard):
                    delcursor.deleteRow()
                    delete_count+=1

print("Deleted " + str(delete_count)+ " relates")
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "Dissolve_Analyisis"
##workspace = arcpy.env.workspace = origin_path
##
##edit = arcpy.da.Editor(workspace)
##edit.startEditing(False, True)
##edit.startOperation()

check_fields = arcpy.ListFields(relationship_tab)

checker_fields = []
diss_data_fields = [temp_origin_field,temp_destin_field]
relate_import_fields = [origin_foreign,dest_foreign]

for field in check_fields:
    checker_fields.append(field.name)


for fied in checker_fields:
    if fied == 'Overlap_SqM':
        relate_import_fields.append(str(fied))
        diss_data_fields.append('SHAPE_Area')
    if fied == 'Overlap1_Per':
        relate_import_fields.append(str(fied))
        diss_data_fields.append(temp_origin_perc)
    if fied == 'Overlap2_Per':
        relate_import_fields.append(str(fied))
        diss_data_fields.append(temp_destin_perc)
    if fied == 'Overlap_Per':
        relate_import_fields.append(str(fied))
        diss_data_fields.append(temp_origin_perc)

arcpy.AddMessage("Fields from dissolve to be imported: " + str(diss_data_fields))
arcpy.AddMessage("Fields to be updated in relates table are: " + str(relate_import_fields))

with arcpy.da.SearchCursor(dissFC,diss_data_fields) as scur:
    with arcpy.da.InsertCursor(relationship_tab,relate_import_fields) as icur:
        for row in scur:
            icur.insertRow(row)

del(row)
del(check_fields)
del(scur)
del(icur)

#close edit session
edit.stopOperation()
edit.stopEditing(True)

#clear scratch workspace
arcpy.Delete_management(dissFC)
arcpy.Delete_management(WorkFolder)
arcpy.AddMessage("Script Complete")

##edit.stopOperation()
##edit.stopEditing(True)