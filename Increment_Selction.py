#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     19/08/2019
# Copyright:   (c) UKPXR011 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Import arcpy module
import arcpy

InputTable = 'C:\Users\UKPXR011\Desktop\Paddy_Work\GSSGISK-422\GSSGISK-422.gdb\Test'
GroupField = 'BoundaryCodeID'
InputField = 'DataDrivenPages_Index'

InputFeature= arcpy.MakeFeatureLayer_management(InputTable,"Feature")

with arcpy.da.SearchCursor(InputFeature, [GroupField]) as cursor:
    myValues = sorted({row[0] for row in cursor})

pStart = 1

for i in myValues:

        selection = (str(GroupField) + " = " +str(i))
        selected = arcpy.SelectLayerByAttribute_management(InputFeature, "NEW_SELECTION", selection)

        #print ("selected "+selection)
        NumS = str(arcpy.GetCount_management(InputFeature))
        Num = int(NumS)
        print Num

        for i in len(NumS):

        #fieldValue = (Num - (Num-pStart))
        # Process: Calculate Field

            arcpy.CalculateField_management(InputTable, InputField, str(i), "PYTHON")

            print(i)



