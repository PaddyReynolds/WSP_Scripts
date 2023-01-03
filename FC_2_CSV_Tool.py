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


env.workspace = arcpy.env.workspace = arcpy.GetParameterAsText(0)
fcList = []
datasetList = arcpy.ListDatasets('*','Feature')
for dataset in datasetList:
    arcpy.env.workspace = dataset
    fcListTemp = arcpy.ListFeatureClasses()
    for fc in fcListTemp:
        feature = str(arcpy.env.workspace) + "\\" + fc
        fcList.append(feature)


csv_out = arcpy.env.workspace = arcpy.GetParameterAsText(0)
with open(csv_out, 'wb') as f:
    writer = csv.writer(f)
    for val in fcList:
        writer.writerow([val])
