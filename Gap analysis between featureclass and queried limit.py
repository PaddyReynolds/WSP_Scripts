#-------------------------------------------------------------------------------
# Name:        Gap analysis between featureclass and queried limit
# Purpose:     Creates a feature class called 'Gaps_Exploded' containing the gaps within the specified limit query of the feature class.
#
# Author:      UKALP001
#
# Created:     15/11/2019
# Copyright:   (c) UKALP001 2019
# Licence:     
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
os.makedirs(desktopPath + "\\Gaps_Find_Folder_" + str(Date))
TempFolder = desktopPath + "\\Gaps_Find_Folder_" + str(Date)
WorkFolder = TempFolder
GDB = "Gaps_LOP"
WorkGDD = WorkFolder + "\\" + GDB + ".gdb"
arcpy.CreateFileGDB_management(TempFolder,GDB)
arcpy.env.workspace = WorkGDD

#Import Layers as variables for view in a toolbox
Input_feature = arcpy.GetParameterAsText(0)
Input_feature2 = arcpy.GetParameterAsText(1)
limit_selection = arcpy.GetParameterAsText(2) 

#Import layers


fc_name = str(os.path.basename(Input_feature).split('\\')[0])

arcpy.AddMessage(' Importing feature class ' + fc_name + ' to be checked for gaps ')

arcpy.FeatureClassToFeatureClass_conversion(Input_feature,WorkGDD,"Input_Features")

arcpy.AddMessage(' Importing queried limits ')

arcpy.FeatureClassToFeatureClass_conversion(Input_feature2,WorkGDD,"Input_Features2",limit_selection)

arcpy.AddMessage(' Imports complete ')

#datasources
FC1 = "Input_Features"
FC2 = "Input_Features2"

#inFeatures are inputs for union, outFeatures is the union output
inFeatures = [FC1,FC2]
outFeatures = "Union_analysis"

#Run union analysis on features
arcpy.AddMessage(' Running union analysis on features')

arcpy.Union_analysis(inFeatures,outFeatures)
field = 'FID_Input_Features'

arcpy.AddMessage(' Union Complete ')

#Delete features which are not gaps
arcpy.AddMessage(' Removing features which are not gaps ')

with arcpy.da.UpdateCursor(outFeatures,field) as cursor:
	for row in cursor:
		if row[0] > -1:
			cursor.deleteRow()

#Explode gaps
arcpy.AddMessage(' Exploding gaps ')

arcpy.MultipartToSinglepart_management(outFeatures,'Gaps_Exploded')

arcpy.AddMessage(' Exploding gaps complete ')

#Count how many gaps
arcpy.AddMessage(' Counting gaps ')

Gap_Count = arcpy.GetCount_management('Gaps_Exploded')
GCount=int(Gap_Count.getOutput(0))
arcpy.AddMessage(str(GCount) + ' Gaps within limit selection ')


