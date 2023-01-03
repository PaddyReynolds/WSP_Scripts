#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKKXR602
#
# Created:     09/01/2020
# Copyright:   (c) UKKXR602 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import os

#Date
now = datetime.datetime.now()
Date = now.strftime("%Y%m%d%H%M")
startTime = datetime.datetime.now()

#Create work space
desktopPath = os.environ.get( "USERPROFILE" ) + "\\Desktop"
os.makedirs(desktopPath + "\\Parish_Stats_" + str(Date))
TempFolder = desktopPath + "\\Parish_Stats_" + str(Date)
WorkFolder = TempFolder
GDB = "Parish_By_Parcel"
WorkGDD = WorkFolder + "\\" + GDB + ".gdb"
arcpy.CreateFileGDB_management(TempFolder,GDB)

#Feature classes to run analysis on
Land_Parcels = r"C:\Users\KRussell\Desktop\HS2B\20200109\GDD.gdb\BackUp\LOP"
Parish_FC = r"C:\Users\KRussell\Desktop\HS2B\20200109\GDD.gdb\BackUp\Parish"
limit_layer = r"C:\Users\KRussell\Desktop\HS2B\20200109\GDD.gdb\BackUp\Limits"

#Variables
Copy_LOP = "LandOwnershipParcels"
Copy_Parish = "Parish"
Copy_Limit = "Limits"
Intersect_output = "Intersected_Parcel_Parish"
Dissolved_input = "Dissolved_Input"
Dissolved_output ="Dissolved_Parcel_Parish"
limit_int = "Limit_Int"
Shape_Area = "SHAPE@AREA"
targetXL = WorkFolder + "\\" + "ParishOutput.xlsx"

#Get parish name and create FC Copy per parish and make local copy of LOP
arcpy.env.workspace = WorkGDD
arcpy.CopyFeatures_management(Land_Parcels,Copy_LOP)
arcpy.CopyFeatures_management(Parish_FC,Copy_Parish)
arcpy.FeatureClassToFeatureClass_conversion(limit_layer,WorkGDD,Copy_Limit,
            "LimitDescription = 'CP3 CCB v4 including Tunnel Section'")

#Run intersect and dissolve, then calculate the original area etc
arcpy.Intersect_analysis([Copy_Limit,Copy_LOP],limit_int,"ALL","","INPUT")
arcpy.Dissolve_management(limit_int,Dissolved_input,['OwnershipReferenceNumber'],"","MULTI_PART","")
arcpy.Intersect_analysis([Copy_Parish,Dissolved_input],Intersect_output,"ALL","","INPUT")
arcpy.Dissolve_management(Intersect_output,Dissolved_output,['Admin3','OwnershipReferenceNumber'],"","MULTI_PART","")
arcpy.AddField_management(Dissolved_output,"Orig_Area","DOUBLE","","","","","NULLABLE")
arcpy.AddField_management(Dissolved_output,"Percent_In","DOUBLE","","","","","NULLABLE")


#Calculate the Original area vs dissolved area to calculate the percentage in
dest_valDict = {r[0]:(r[1:])for r in arcpy.da.SearchCursor(Copy_LOP,["OwnershipReferenceNumber",Shape_Area])}
with arcpy.da.UpdateCursor(Dissolved_output,["OwnershipReferenceNumber","Orig_Area"]) as updateRows:
    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in dest_valDict:
            updateRow[1] = dest_valDict[keyValue][0]
            updateRows.updateRow(updateRow)

#Calculating Percentage
try:
    with arcpy.da.UpdateCursor(Dissolved_output,["Orig_Area","SHAPE_Area","Percent_In"]) as cursor:
        for row in cursor:
            if row[1] >= row[0]:
                row[2] = 100
            else:
                row[2] = (row[1] * 100) / row[0]
            cursor.updateRow(row)
except:
    arcpy.AddMessage("Error Calcuating origin percentage field")

#Convert Feauture class to array
Fields_to_Keep = ['OwnershipReferenceNumber','Admin3',"SHAPE_Area","Orig_Area","Percent_In"]
df = pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(Dissolved_output,Fields_to_Keep))

print df

#Create a list of all the parish's in the dissolve
list_parish = []

with arcpy.da.SearchCursor(Dissolved_output,'Admin3') as cursor:
    for row in cursor:
        list_parish.append(str(row[0]))

list_parish = list(set(list_parish))
print list_parish

#Loop through the list
Sheet_count = 0
df = pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(Dissolved_output,Fields_to_Keep))
pd.set_option('display.max_colwidth', 40)
writer = pd.ExcelWriter(targetXL,engine='xlsxwriter')

for par in list_parish:
    Sheet_count+=1
    Parish_name = str(par)
    Removed = Parish_name.replace("Parish of ", "")
    reduced_list = Removed[0:30]
    df_name = 'df' + str(Sheet_count)
    df_name = pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(Dissolved_output,Fields_to_Keep))
    sheet = reduced_list
    data = df_name.loc[df_name['Admin3'] == par ]
    data.to_excel(writer,index=False ,sheet_name= sheet)
    del df_name
writer.save()


