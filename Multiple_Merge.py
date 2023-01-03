#-------------------------------------------------------------------------------
# Name:        module3
# Purpose:
#
# Author:      UKPXR011
#
# Created:     14/01/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
arcpy.env.workspace = r'C:\Users\UKPXR011\Desktop\Scratch\Parish_Update\Parish_Unsplit.gdb' # Replace correct geodatabase path
arcpy.env.overwriteOutput = True

fc = r'C:\Users\UKPXR011\Desktop\Scratch\Parish_Update\Parish_Unsplit.gdb\Unsplit_Test_1'
fc1 = r'C:\Users\UKPXR011\Desktop\Scratch\Parish_Update\Parish_Unsplit.gdb\Ownership_Dissolved'
fc2 = r'C:\Users\UKPXR011\Desktop\Scratch\Parish_Update\Parish_Unsplit.gdb\Unsplit_Test_Schema'
#fc2 =r'C:\Users\UKPXR011\Desktop\Scratch\Parish_Update\Parish_Unsplit.gdb\Unsplit_Test_Schema_1'
fc3 =  r'C:\Users\UKPXR011\Desktop\Scratch\Parish_Update\Parish_Unsplit.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'
# Make a copy of the original feature class
arcpy.Copy_management(fc, fc2)

fc4= arcpy.Dissolve_management(fc,fc1,['OwnershipReferenceNumber'])


fields = ['OwnershipReferenceNumber', 'SectionID', 'SheetNo', 'SpatialCategoryID', 'BoundaryCodeID', 'Tenure', 'SymColour', 'Status', 'ExternalReference', 'ModifiedBy', 'ModifiedDate', 'ExtentMinX', 'ExtentMinY', 'ExtentMaxX', 'ExtentMaxY', 'CentroidX', 'CentroidY', 'DataDrivenPages_Index', 'AutoNumber', 'created_user', 'created_date', 'last_edited_user', 'last_edited_date', 'GlobalID', 'Temp_Notes', 'PreviousOwnRefNo', 'Sub_Project', 'PinPoint_URL', 'StreetView_URL']

# Empty FC to append dissolved features into.
nodeList = []
with arcpy.da.UpdateCursor(fc2, ['OwnershipReferenceNumber']) as cursor:
    for row in cursor:
        cursor.deleteRow()

arcpy.Append_management(fc4,fc2, "NO_TEST")


#Calculate the Original area vs dissolved area to calculate the percentage in
valueDict = {r[0]:(r[1:])for r in arcpy.da.SearchCursor(fc3,fields)}

with arcpy.da.UpdateCursor(fc2,fields) as updateRows:

    for updateRow in updateRows:

        keyValue = updateRow[0]

        if keyValue in valueDict:

            for n in range (1,len(fields)):

                updateRow[n] = valueDict[keyValue][n-1]

            updateRows.updateRow(updateRow)




print "Paddy you're a Genius"
