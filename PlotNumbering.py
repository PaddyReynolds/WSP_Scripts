#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKKXR602
#
# Created:     27/10/2019
# Copyright:   (c) UKKXR602 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
import shutil
from datetime import datetime


fc = arcpy.GetParameterAsText(0)
fc3 = arcpy.GetParameterAsText(1)
field = 'Parish'
field_to_update = "LandReferenceNo"
DissolveField= 'UniqueID'
DissolveFieldStats = 'Number MIN'
Page_Number = "MIN_Page1"
X_field = "X"
Y_field = "Y"
decimals = 0

#Create local GDB & work folders
arcpy.AddMessage("Creating Local Copy")
desktopPath = os.environ.get( "USERPROFILE" ) + "\\Desktop"
os.makedirs(desktopPath + "\\PlotNumberingScratch")
TempFolder = desktopPath + "\\PlotNumberingScratch"
ScratchGDD = "PlotScratch"
WorkGDD = TempFolder + "\\" + ScratchGDD + ".gdb"
dissolvedPlots = WorkGDD + "\\" + "DissolvedPlots"
arcpy.CreateFileGDB_management(TempFolder,ScratchGDD)

#dissolve plots to get a list of parishes in the project
arcpy.AddMessage("Dissolving Plots to Generate Parcel List to Number Plots")
arcpy.Dissolve_management(fc,dissolvedPlots,field,"",)

#set dissolvedPlots to be one of the fc required for numbering
fc2 = dissolvedPlots

#Intersect Pages with plots, dissolve to get minimum page for each plot and name each accordingly
fc4 = WorkGDD + "\\" + "Plot_page_intersect"
fc5 = WorkGDD + "\\" + "Plot_page_intersect_Dissolve"

#List of features to be intersected
infeatures = [fc, fc3]

#Intersect infeatures with NO_FID attached and no other parameters
arcpy.Intersect_analysis (infeatures, fc4, "NO_FID", "", "")

#Dissolve the intersect feature baised on the unique ID with the statistics applied to record the minimum page number.
arcpy.Dissolve_management(fc4,fc5,DissolveField,DissolveFieldStats,"","")


'''
Set up an update cursor which will transfer the minimum page number from the intersected dissolved
layer into the original plots layer
'''

#Fields containing join field and the updated field
sourceFieldsList = [DissolveField, "MIN_Number"]

# A dictionary storing the vaules from the table with the field containing the join field and the updated field
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc5, sourceFieldsList)}

#Fields containing the join field and the field containing the updated values
updateFieldsList = [DissolveField,Page_Number]

with arcpy.da.UpdateCursor(fc, updateFieldsList) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

del valueDict


#Auto Number Plots from South to North
arcpy.AddMessage("Auto Numbering Plots from South to North")

#Cursor of Parishes
cursor = arcpy.SearchCursor(fc2)


for row1 in cursor:
    #Parish List within Plots adn makes querey
    parishes = str(row1.getValue(field))
    query = str(field) + " ='" + parishes + "'"
    #Grabs Page Number (from fishnet) and X, Y and OID
    coords = [[i[0],i[1],i[2],i[3]] for i in arcpy.da.SearchCursor(fc,[Page_Number,Y_field,X_field,"OID@"],query)]
    #Sorts everything (- conversts to negative)
    coords.sort( key=lambda k:(round(k[0],decimals),round(k[1],decimals),round(-k[2],decimals)))
    #Pulls ODI
    order = [i[0] for i in coords]
    #Joins sorted list back to original and counts
    d ={k:v for (v,k) in list(enumerate(order))}
    #print(Parish_List)

    with arcpy.da.UpdateCursor(fc,["OID@",field_to_update]) as cursor:
        for row in cursor:
            row[1] = int(d[row[0]]+1)
            cursor.updateRow(row)
print ("Done")