#-------------------------------------------------------------------------------
# Name:        Licence Sliver Finder
# Purpose:     Detect potential sliver's in HS2 databases and produce report
#              highlighting Licence Layers to be reviewed.
#
# Author:      Kane Russell
#
# Created:     04/04/2019
# Copyright:   (c) UKKXR602 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, os
from arcpy import env
import shutil

#create scratch folder, then set as work environment
desktopPath = os.environ.get( "USERPROFILE" ) + "\\Desktop"
os.makedirs(desktopPath + "\\LicenceSliverScratch")
TempFolder = desktopPath + "\\LicenceSliverScratch"
arcpy.env.scratchworkspace = TempFolder

#Set Variables
ScratchGDD = "ScratchGDD_Sliver.gdb"
WorkGDD = TempFolder + "\\" + ScratchGDD
inputShapeFile = r"C:\Users\UKPXR011\Desktop\Current Work\2b\AP2\CLS\Slivers\Scratch.gdb\AP2_CLS"
Location = "C:\Users\UKPXR011\Desktop\Current Work\2b\AP2\CLS\Slivers"
Output_Location = WorkGDD
outputShapeFileName = "Licences"
Report = Location + "\\" +"LicenceSliverReport.xls"
Licence_Layer = WorkGDD + "\\Licences"

#Create GDD
arcpy.AddMessage("Creating Scratch GDB")
arcpy.CreateFileGDB_management(TempFolder,ScratchGDD)

# List of the fields to keep in Licence Copy
arcpy.AddMessage("Copying Licence Feature to Scratch Workspace")
outputFields = ["TOID"]
properties = "EXTENT"
length_unit = ""
area_unit = ""
coordinate_system = ""


fieldMappings = arcpy.FieldMappings()

# create the field mappings from the outputFields list.
# only fields in the list will be included in the exported shape file.
for field in outputFields:
    fieldMap = arcpy.FieldMap()
    fieldMap.addInputField(inputShapeFile, field)
    fieldMappings.addFieldMap(fieldMap)

# Use FeatureClassToFeatureClass and apply the fieldMappings
arcpy.FeatureClassToFeatureClass_conversion(inputShapeFile,
                                            Output_Location,
                                            outputShapeFileName,
                                            "",
                                            fieldMappings,
                                            "")

#Set expression
FieldName = "Slither"
expression = "Reclass(!Combined_Value!)"
codeblock = """
def Reclass(WellYield):
    if (WellYield >= 0 and WellYield <= 1):
        return 'Highly Unlikely Sliver'
    elif (WellYield > 1 and WellYield <= 3):
        return 'Low Probability Sliver'
    elif (WellYield > 3 and WellYield <= 10):
        return 'Potential Sliver'
    elif (WellYield > 10 and WellYield <= 50):
        return 'Probably Sliver'
    elif (WellYield > 50 and WellYield <= 100):
        return 'Likely Sliver'
    elif (WellYield > 100):
        return 'Highly Likely Sliver'"""

#Calculate Sliver Probability
arcpy.AddMessage("Calculating Geometry")
arcpy.AddGeometryAttributes_management(Licence_Layer,properties,area_unit,coordinate_system)
arcpy.AddField_management(Licence_Layer,"Compared_X","DOUBLE")
arcpy.AddField_management(Licence_Layer,"Compared_Y","DOUBLE")
arcpy.AddField_management(Licence_Layer,"Combined_Value","DOUBLE")
arcpy.AddField_management(Licence_Layer,"Sliver","TEXT","","","","Sliver","NULLABLE","REQUIRED")
arcpy.CalculateField_management(Licence_Layer,"Compared_X","[EXT_MAX_X] - [EXT_MIN_X]","VB","")
arcpy.CalculateField_management(Licence_Layer,"Compared_Y","[EXT_MAX_Y] - [EXT_MIN_Y]","VB","")
arcpy.CalculateField_management(Licence_Layer,"Combined_Value","[Compared_Y] + [Compared_X]","VB","")
arcpy.CalculateField_management(Licence_Layer,"Combined_Value","[Combined_Value] / [SHAPE_Area]","VB","")
arcpy.CalculateField_management(Licence_Layer,FieldName,expression,"PYTHON_9.3",codeblock)
arcpy.DeleteField_management(Licence_Layer, drop_field="EXT_MIN_X;EXT_MIN_Y;EXT_MAX_X;EXT_MAX_Y;Compared_X;Compared_Y;Combined_Value")

#Export report to excel
arcpy.AddMessage("Export Report")
arcpy.TableToExcel_conversion(Licence_Layer,Report,"ALIAS","DESCRIPTION")

#Delete Scratch Folder
shutil.rmtree(TempFolder)