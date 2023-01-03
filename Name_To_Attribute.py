#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      UKPXR011
#
# Created:     30/10/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
file_name_field = 'CLRID'
input_gdb_or_folder = r'C:\Users\UKPXR011\Desktop\Current Work\2A\LAA\08112021'

arcpy.env.workspace = input_gdb_or_folder

feature_classes = arcpy.ListFeatureClasses()

for fc in feature_classes:
    print(fc) # just so you know what the script is processing

    # add field to hold the file name if it does not exist
    existing_fields = [f.name for f in arcpy.ListFields(fc)]
    if file_name_field not in existing_fields:
        arcpy.management.AddField(fc, file_name_field, 'TEXT', field_length=200)

    # write the file name into each row of the file name filed
    with arcpy.da.UpdateCursor(fc, [file_name_field]) as uc:
        for row in uc:
            uc.updateRow([str(fc)])
    del row, uc

