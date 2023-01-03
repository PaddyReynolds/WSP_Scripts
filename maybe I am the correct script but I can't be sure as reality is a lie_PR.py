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

fc = r"C:\Users\UKPXR011\Desktop\Scripts\PlotDataSet\PlotDataSet.gdb\Plot_Page_Test"
fc2 = r"C:\Users\UKPXR011\Desktop\Scripts\PlotDataSet\PlotDataSet.gdb\Dissolve"

field = 'Parish'
field_to_update = "LandReferenceNo"
Page_Number = "MIN_Page1"
X_field = "X"
Y_field = "Y"
decimals = 0

#Auto Number Plots from South to North
arcpy.AddMessage("Auto Numbering Plots from South to North")
cursor = arcpy.SearchCursor(fc2)

testlist = []

for row1 in cursor:
    #Parish List within Plots adn makes querey
    parishes = str(row1.getValue(field))
    #ParishList = parishes + '_list'
    #Parish_List = ParishList = []
    query = str(field) + " ='" + parishes + "'"
    #Grabs Page Number (from fishnet) and X, Y and OID
    coords = [[i[0],i[1],i[2],i[3]] for i in arcpy.da.SearchCursor(fc,[Page_Number,Y_field,X_field,"OID@"],query)]
    #Sorts everything (- conversts to negative)
    coords.sort( key=lambda k:(round(k[0],decimals),round(k[1],decimals),round(-k[2],decimals)))
    #Pulls ODI
    order = [i[3] for i in coords]
    #Joins sorted list back to original and counts
    d ={k:v for (v,k) in list(enumerate(order))}
    #print(Parish_List)

    with arcpy.da.UpdateCursor(fc,["OID@",field_to_update],query) as cursor:
        for row in cursor:
            row[1] = int(d[row[0]]+1)
            cursor.updateRow(row)

#Delete superflous data & lockfiles
##del(row)
##del(row1)