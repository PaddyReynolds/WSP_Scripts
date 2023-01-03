#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKKXR602
#
# Created:     10/01/2020
# Copyright:   (c) UKKXR602 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import os

#GDD to export features from
GDD_To_export = arcpy.GetParameterAsText(0)

#XLS to export
targetXL = arcpy.GetParameterAsText(1)

#Make workspace
arcpy.env.workspace = GDD_To_export

fc_List = arcpy.ListFeatureClasses()

writer = pd.ExcelWriter(targetXL,engine='xlsxwriter')

counter = 0

for fc in fc_List:
    counter+=1
    sheet_Names = os.path.basename(fc).split('\\')[0]
    featurename = os.path.basename(fc).split('\\')[0]
    list = featurename = []
    Fields_to_keep = arcpy.ListFields(fc)
##    for fld in Fields_to_keep:
##        names = fld.name
##        list.append(str(names))
    df_name = 'df' + str(counter)
    df_name = pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(fc,
                [fld.name for fld in arcpy.ListFields(fc) if fld.name != arcpy.Describe(fc).shapeFieldName]))
    sheet = str(sheet_Names)
    df_name.to_excel(writer,index=False ,sheet_name= sheet_Names)

writer.save()


