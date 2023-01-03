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
arcpy.AddMessage("Auto Numbering Plots from South to North")
cursor = arcpy.SearchCursor(fc2)

testlist = []

for row1 in cursor:
    parishes = str(row1.getValue(field))
    ParishList = parishes + '_list'
    Parish_List = ParishList = []
    query = str(field) + " ='" + parishes + "'"
    coords.sort( key=lambda k:(round(k[0],decimals),round(k[1],decimals),round(-k[2],decimals)))
    order = [i[3] for i in coords]
    d ={k:v for (v,k) in list(enumerate(order))}
    print(ref)
    print(d)
    with arcpy.da.UpdateCursor(fc,["OID@",field_to_update],query) as cursor:
        for row in cursor:
            row[1] = int(d[row[0]]+1)
            cursor.updateRow(row)
##    for r,ele in enumerate(ref):
##        appendin = r,ele
##        Parish_List.append(appendin)
##    T1 = list(Parish_List)
##    print(ref)

##    print(Parish_List)
##    with arcpy.da.UpdateCursor(fc,["OID@",field_to_update],query) as cursor:
##       for row in cursor:
##            if  OID_Sorted == row[0]:
##                row[1] = int(Plot_Number[0])+1
##                cursor.updaterow(row)
    ##    d = {x:v for (v,x) in order}
##    with arcpy.da.UpdateCursor(fc,["OID@",field_to_update],query) as cursor:
##        for row in cursor:
##            row[1] = int(d[row[0]]+1)
##            cursor.updateRow(row)

#Delete superflous data & lockfiles
##del(row)
##del(row1)