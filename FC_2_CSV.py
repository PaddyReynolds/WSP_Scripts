#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     16/08/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import csv, arcpy, os
from arcpy import env

workspace = r'C:\Users\UKPXR011\Desktop\Scripts\FC_2_CSV\2DE01-MWJ-GI-GDD-M000-000053_P07\2DE01-MWJ-GI-GDD-M000-000053_P07\CP3.1.gdb'
env.workspace = workspace
fcList = []
features = arcpy.ListFeatureClasses("*")


for fc in features:
        feature = fc
        fcList.append(feature)

csv_out = 'C:\Users\UKPXR011\Desktop\Scripts\FC_2_CSV\FC_2_CSV.csv'
with open(csv_out, 'wb') as f:
    writer = csv.writer(f)
    for val in fcList:
        writer.writerow([val])
