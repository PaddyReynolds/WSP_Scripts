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

fc = r"C:\Users\KRussell\Desktop\Developing\Plot Numbering\version2.0\PlotDataSet.gdb\Plot"
fc2 = r"C:\Users\KRussell\Desktop\Developing\Plot Numbering\version2.0\PlotDataSet.gdb\Dissolve"

field = 'Parish'
field_to_update = "LandReferenceNo"
Page_Number = "MIN_Page1"
X_field = "X"
Y_field = "Y"



#Auto Number Plots from South to North
##arcpy.AddMessage("Auto Numbering Plots from South to North")
##cursor = arcpy.SearchCursor(fc2)
##for row1 in cursor:
##    parishes = str(row1.getValue(field))
##    query = str(field) + " ='" + parishes + "'"
##    coords = [[round(i[0],0),round(i[1],0),i[3]] for i in arcpy.da.SearchCursor(fc,[Page_Number,Y_field,X_field,"OID@"],query)]
##    coords.sort(key=lambda k: (k[1],-k[0]), reverse=True)
##    order = [i[2] for i in coords]
##    d = {k:v for (v,k) in list(enumerate(order))}
##    with arcpy.da.UpdateCursor(fc,["OID@",field_to_update],query) as cursor:
##        for row in cursor:
##            row[1] = int(d[row[0]]+1)
##            cursor.updateRow(row)

#Delete superflous data & lockfiles
del(row)
del(row1)