#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     30/11/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os

file_Path = arcpy.GetParameterAsText(0)

os.makedirs(file_Path +"\\"+"Will_This_Work")
TempFolder = file_Path + "\\"+"Will_This_Work"

arcpy.CreateFolder_management(file_Path,"test")