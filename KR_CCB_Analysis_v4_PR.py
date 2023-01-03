#-------------------------------------------------------------------------------
# Name:        CCB Sliver Analysis Script (KR Draft)
# Purpose:     Checks current CCB against an existing feature class
#              namely the LandOwnership Parcels & Access Licence Layer
# Author:      UKKXR602
#
# Created:     30/08/2019
# Copyright:   (c) UKKXR602 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
import datetime
import arcpy_metadata as md

#Date
now = datetime.datetime.now()
Date = now.strftime("%Y%m%d%H%M")
Date2 = now.strftime("%d/%m/%Y")
Date3 = now.strftime("%d%m%Y")

#Set input parameters
input_ccb_limit = arcpy.GetParameterAsText(0)
input_LOP_FC = arcpy.GetParameterAsText(1)
output_location = arcpy.GetParameterAsText(2)
Dissolve_field = arcpy.GetParameterAsText(3)
GIS_Analyst = str(arcpy.GetParameterAsText(4))

#set variables
arcpy.AddMessage("Create analysis workspace")
Work_FolderName = "CCB_Analysis_" + str(Date)
WorkSpace = output_location + "\\" + Work_FolderName
OutputFolderName = "Output_CCB_Analysis_" + str(Date3)
Output_Folder = WorkSpace + "\\" + OutputFolderName
GDD_Name = "CCB_Sliver_Analysis.gdb"
OutputGDD_Name = "CCB_AnalysisReport_" + str(Date3) + ".gdb"
OutputGDD = Output_Folder + "\\" + OutputGDD_Name
Meta_data_layer = WorkSpace + "\\" + GDD_Name + "\\" + "CCB_Exploded_Output"
Geometry_layer = WorkSpace + "\\" + GDD_Name + "\\" + "CCB_Exploded_Output"
Report = Output_Folder + "\\" +"CCBSliverReport.xls"

#Slither Variables
arcpy.AddMessage("Copying Licence Feature to Scratch Workspace")
properties = "EXTENT"
length_unit = ""
area_unit = ""
coordinate_system = ""

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

#Create Workspace and set work environment
arcpy.CreateFolder_management(output_location,Work_FolderName)
arcpy.CreateFileGDB_management(WorkSpace,GDD_Name)
arcpy.env.workspace = WorkSpace + "\\" + GDD_Name

#Intersect Input FC against Input CCB Boundary then run slither analysis on exploded output
arcpy.AddMessage("Run CCB Analysis against selected input FC and " + str(Dissolve_field) + " field")
arcpy.Intersect_analysis([input_LOP_FC,input_ccb_limit],"InputFC_CCB_Int","ALL","","INPUT")
arcpy.Dissolve_management("InputFC_CCB_Int","CCB_Dissolve_Output",Dissolve_field,"","MULTI_PART","")
arcpy.AddField_management("CCB_Dissolve_Output","Perc_in_input","SHORT","","","","Percentage in","NULLABLE","NON_REQUIRED")
arcpy.MakeFeatureLayer_management(input_LOP_FC,input_LOP_FC + "_view")
arcpy.MakeFeatureLayer_management("CCB_Dissolve_Output","CCB_Dissolve_Output_view")
arcpy.JoinField_management("CCB_Dissolve_Output_view",Dissolve_field,input_LOP_FC + "_view",Dissolve_field,['Shape_Area'])
arcpy.CalculateField_management("CCB_Dissolve_Output_view","Perc_in_input","[Shape_Area] / [Shape_Area_1] *100","VB","")
arcpy.MultipartToSinglepart_management("CCB_Dissolve_Output","CCB_Exploded_Output")
arcpy.AddMessage("Calculating Geometry")
arcpy.AddGeometryAttributes_management(Geometry_layer,properties,area_unit,coordinate_system)
arcpy.AddField_management(Geometry_layer,"Compared_X","DOUBLE")
arcpy.AddField_management(Geometry_layer,"Compared_Y","DOUBLE")
arcpy.AddField_management(Geometry_layer,"Combined_Value","DOUBLE")
arcpy.AddField_management(Geometry_layer,"Slither","TEXT","","","","Slither?","NULLABLE","REQUIRED")
arcpy.CalculateField_management(Geometry_layer,"Compared_X","[EXT_MAX_X] - [EXT_MIN_X]","VB","")
arcpy.CalculateField_management(Geometry_layer,"Compared_Y","[EXT_MAX_Y] - [EXT_MIN_Y]","VB","")
arcpy.CalculateField_management(Geometry_layer,"Combined_Value","[Compared_Y] + [Compared_X]","VB","")
arcpy.CalculateField_management(Geometry_layer,"Combined_Value","[Combined_Value] / [SHAPE_Area]","VB","")
arcpy.CalculateField_management(Geometry_layer,FieldName,expression,"PYTHON_9.3",codeblock)
arcpy.DeleteField_management(Geometry_layer, drop_field="EXT_MIN_X;EXT_MIN_Y;EXT_MAX_X;EXT_MAX_Y;Compared_X;Compared_Y;Combined_Value;ORIG_FID")
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "CCB_Exploded_Output"
arcpy.AddGeometryAttributes_management(Geometry_layer,"CENTROID","","","")

#Create output folder where new GDD be be created for client along with report
arcpy.AddMessage("Create output Folder and GDB")
arcpy.CreateFolder_management(WorkSpace,OutputFolderName)
arcpy.CreateFileGDB_management(Output_Folder,OutputGDD_Name)
arcpy.CopyFeatures_management(Geometry_layer,OutputGDD + "\\" + "CCB_Analysis")

#Export Output to excel format
arcpy.AddMessage("Export Report")
arcpy.TableToExcel_conversion(OutputGDD + "\\" + "CCB_Analysis",Report,"ALIAS","DESCRIPTION")
arcpy.AddMessage("Update Metadata")

#Get name of GDD  for Metadata input
desc = arcpy.Describe(input_ccb_limit)
GDD_Path = desc.path
gdd_Name = os.path.basename(GDD_Path).split('\\')[0]

#Abstract for updating feature Metadata
Analysis_Abstract = """CCB Analysis Report:

Report ran on {} supplied by HS2 with analysis ran on {} by {}.

Report is ran to detect slivers within input feature class against CCB boundary.

The script using ESRI Tools (Intersect & Dissolve) to calculate the area and percentage of input Feature Class against CCB.

The overlap area of Feature Class within CCB is then converted to single part with geometry tested to predict probability of sliver.""".format(gdd_Name,Date2,GIS_Analyst)

metadata = md.MetadataEditor(OutputGDD + "\\" + "CCB_Analysis")

metadata.title = "CCB Analysis"
metadata.purpose = "WSP CCB Sliver analysis"
metadata.abstract = Analysis_Abstract
metadata.credits = "WSP"
metadata.limitation = "For information Purposes Only."
metadata.finish()