#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     08/11/2022
# Copyright:   (c) UKPXR011 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     23/09/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env, mapping
import os

MXDName = r'C:\Users\UKPXR011\Desktop\Current Work\2b\AP2\CLS\Small_Plots.mxd'
LayersList = []

mxd = mapping.MapDocument(MXDName)
lyrs = mapping.ListLayers(mxd)
print MXDName

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DATASOURCE"):
        source = lyr.dataSource
        LayersList.append(source)


with open(r"C:\Users\UKPXR011\Desktop\Current Work\2b\AP2\CLS\Layers_QC.txt", 'w') as f:
    for item in LayersList:
        f.write("%s\n" % item)

