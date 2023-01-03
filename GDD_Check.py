#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      UKPXR011
#
# Created:     07/02/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import pandas as pd
import datetime
import os
arcpy.env.overwriteOutput = True

#List to Hold Errors
Errors = []
#List to hold Lnumbers
Lnumbers = []
#Current Date and Time
date_formated =str(pd.to_datetime('now'))
#count of Errors
ErrorCount = 0

# Change the workspace to where you would like the Project folder to be saved
workspace = r"C:\Users\UKPXR011\Desktop\Current Work\QC\2B Leeds\GDD_QC"

# Change the name of the folder to the Project name
projectname = "GGD_Check"

desktopPath = r"C:\Users\UKPXR011\Desktop\Current Work\QC\2B Leeds\GDD_QC"
ScratchGDD = "GDD_QC_2021"
WorkGDD = desktopPath + "\\" + ScratchGDD + ".gdb"
if os.path.exists(WorkGDD) == False:
    arcpy.CreateFileGDB_management(desktopPath,ScratchGDD)

fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\QC\2B Leeds\2C866-WSP-GI-GDD-L000-000003 _P10\2C866-WSP-GI-GDD-L000-000003 _P10\Y21W33.gdb\PRP_WSP_2C866_LD_LandAccess_Ply'
fc2 = str(WorkGDD)+'\\Overlaps'
fc3 = str(WorkGDD)+'\\Multiparts'
fc4= str(WorkGDD)+'\\Geometry'
#fc5 = r'C:\Users\UKPXR011\Desktop\QC Work\GDD_QC\Scratch.gdb\CP3'
fc6 = str(WorkGDD)+'\\DissolvedGDD'
fc7 = str(WorkGDD)+'\\Union1'
fc8 = str(WorkGDD)+'\\ExplodedUnion'
QC_Fields = ['TitleNum','LicenceNum','Status','ExpiryDate','Expired']


with arcpy.da.SearchCursor(fc1,QC_Fields) as cursor:

    for row in cursor:

        Lnumbers.append(row[1])
        #Check that title field has characters in it and is not null or full of blanks
        if  row [0] is None or row[0] == "" or row[0] == " " :
            Errors.append(str(row[1] + " Is Missing a Title Number"))
            ErrorCount =ErrorCount + 1


        #Check all agreed licenses have expiry dates
        if  row[2] =='Agreed' and row [3] is None or row[3] == "" or row[3] == " ":
            Errors.append(str(row[1] + " Has no Expiry Date When its Status is " + row[2]))
            ErrorCount = ErrorCount+1

        #check non agreed licenses dont have expiry dates
        if row[2] <> 'Agreed' and row[3] is not None:
            Errors.append(str(row[1] + " Has an Expiry Date When its Status is " + row[2]))
            ErrorCount = ErrorCount+1


        #Check Expiry Dates are correct
        if row[3] is not None and str(row[3]) > date_formated and (row[4] == 'Yes'):
            Errors.append(str(row[1] + " Is Marked as expired when it has not Expired"))
            ErrorCount =ErrorCount + 1

        if row[3] is not None and str(row[3]) < date_formated and (row[4] == 'No' or row[4] == 'N/A'):
            Errors.append(str(row[1] + " Is Not Marked as expired when it has Expired"))
            ErrorCount =ErrorCount + 1


LSet = set([x for x in Lnumbers if Lnumbers.count(x) > 1])
#Check for Duplicate Lnumbers
if len(LSet) != 0:
    Errors.append("Duplicate Lnumbers")
    ErrorCount =ErrorCount + 1

IntersectFeatures = [fc1,fc1]
#Check for Overlaps
arcpy.Intersect_analysis(IntersectFeatures,fc2)
rows1 = len([row for row in arcpy.da.SearchCursor(fc1,['OBJECTID'])])
rows2 = len([row for row in arcpy.da.SearchCursor(fc2,['OBJECTID'])])
if rows1 != rows2:
    Errors.append("Overlaps")
    ErrorCount =ErrorCount + 1

#Check for Multiparts
arcpy.MultipartToSinglepart_management(fc1, fc3)
rows3 = len([row for row in arcpy.da.SearchCursor(fc3,['OBJECTID'])])
if rows1 != rows3:
    Errors.append("Multiparts")
    ErrorCount =ErrorCount + 1


#Check Geometry
arcpy.CheckGeometry_management (fc1, fc4)
rows4 = len([row for row in arcpy.da.SearchCursor(fc4,['OBJECTID'])])
if rows4 != 0:
    Errors.append("Geometry Errors")
    ErrorCount =ErrorCount + 1


arcpy.Dissolve_management(fc1, fc6)
'''
#Check for Gaps
arcpy.Union_analysis([fc6,fc5],fc7)
UnionFields =['FID_DissolvedGDD','FID_CP3']

GapCounter = 1

with arcpy.da.UpdateCursor(fc7,UnionFields) as cursor:
    for row in cursor:
        if row[0] == -1 and row[1] == 1:
            GapCounter = GapCounter +1
            pass
        else:
            cursor.deleteRow()

if GapCounter != 0:

    arcpy.MultipartToSinglepart_management(fc7,fc8)
    rows5 = len([row for row in arcpy.da.SearchCursor(fc8,['OBJECTID'])])
    Errors.append(str(len(fc8)) +" Gaps in CP3")
    ErrorCount =ErrorCount + len(fc8)

else:
    Errors.append("No Gaps in CP3")
'''

print ErrorCount
print Errors

