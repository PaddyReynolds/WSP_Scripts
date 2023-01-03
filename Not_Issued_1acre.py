#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     05/02/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import pandas as pd

date_formated =str(pd.to_datetime('now'))

#print date_formated
fc1 = r'C:\Users\UKPXR011\Desktop\Stats\Scratch.gdb\AccessLicences'
fields = ['Status','SHAPE_Area','ExpiryDate']

with arcpy.da.UpdateCursor(fc1, fields) as updateRows:
    for updateRow in updateRows:
        if updateRow[0] =='Not Issued':

            if updateRow[1] >= 4046.86:
                updateRow[0] = "Not Issued 1 Acre or Larger"
                updateRows.updateRow(updateRow)

            else:
                updateRow[0] = "Not Issued Under 1 Acre"
                updateRows.updateRow(updateRow)


        elif updateRow[0] =='Agreed':

            if str(updateRow[2]) < date_formated:

                updateRow[0] ='Agreed Expired'
                updateRows.updateRow(updateRow)


            else:
                updateRow[0] ='Agreed Not Expired'
                updateRows.updateRow(updateRow)


        else:
            pass



