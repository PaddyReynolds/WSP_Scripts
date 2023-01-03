#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     22/01/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import system modules
import arcpy
import pandas as pd
from pandas import DataFrame
import xlsxwriter

# Set global variables
arcpy.env.overwriteOutput = True

#Fileds used to create Dictionary
listfields = ["HMLR_Title_No","created_date"]

#HMLR Featureclass
HMLRTitles = r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\SOP_Final.gdb\STATUTORY_PROCESSES\HMLR_Parcels'

#creating a pandas DataFrame that keeps the largest created date for each HMLR title
hmlrDict = pd.DataFrame.from_records(data=arcpy.da.SearchCursor(HMLRTitles,listfields), columns=listfields).sort_values("created_date").groupby("HMLR_Title_No").last()

#Save to excel file
export_excel = hmlrDict.to_excel (r'C:\Users\UKPXR011\Desktop\Safeguarding\SOP\export_dataframe.xlsx', index = "HMLR_Title_No", header=True)

