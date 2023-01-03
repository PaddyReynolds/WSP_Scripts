##################################################
#Inspired by: School of Engineering, University of Zambia (UNZA)
#Survey Community - Zambia (Arc1950)
#Developer: ebenezer.odoi@gmail.com  +16145943273
##################################################


import os
import sys
import arcpy

arcpy.env.overwriteOutput = True
# import pythonaddins


#######User Selection 1
poly_lyr = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\SoS\A101_001_SoS\A101_001.gdb\WillNeverWork'
# poly_lyr = r"C:\Users\EB\Desktop\polygons\Export_OutputPro.shp"

#######User Selection 2
# num_out_polys = 10
num_out_polys = 5
#map units (eg meters) and the difference in area between the largest and the smallest polygons
#0.005 - 0.02%; 0.01 - 0.03%; 0.05 - 0.1%; 0.1 - 0.3%;
step_value = 1

#######User Selection 3
# orientation = 'NS' #'WE' / 'NS'

# number of splits
splits = [round(float(100)/float(num_out_polys), 2)] * num_out_polys

#spatial reference of the output fc will be of the polygon layer
sr = arcpy.SpatialReference(arcpy.Describe(poly_lyr).spatialReference.factoryCode)

#source polygon fields
fields = [f.name for f in arcpy.ListFields(poly_lyr) if not f.required]


#get polygon geometry and extent property
with arcpy.da.SearchCursor(poly_lyr, fields + ["SHAPE@"]) as cur:
    for row in cur:
        attributes = list(row[:-1])
        polygon = row[-1]
        extent = polygon.extent



x_max = extent.XMax
x_min = extent.XMin
y_max = extent.YMax - step_value
y_min = extent.YMin

cut_poly = polygon
lines = []

with arcpy.da.InsertCursor(poly_lyr, fields + ["SHAPE@"]) as icur:
    for i in splits[:-1]: #need to get all but the last item
        tolerance = 0
        while tolerance < i:
            pnt_arr = arcpy.Array()


            #construct West-East oriented line
            pnt_arr.add(arcpy.Point(x_min, y_max))
            pnt_arr.add(arcpy.Point(x_max, y_max))

            line = arcpy.Polyline(pnt_arr, sr)
            lines.append(line)

            #cut polygon and get split-parts
            cut_list = cut_poly.cut(line)


            tolerance = 100 * cut_list[0].area / polygon.area
            y_max -= step_value

        # part 0 is on the right side and part 1 is on the left side of the cut


        cut_poly = cut_list[1]
        icur.insertRow(attributes + [cut_list[0]])


    icur.insertRow(attributes + [cut_list[1]])
del icur

with arcpy.da.UpdateCursor(poly_lyr,['OBJECTID']) as updateRow:
    for updateRows in updateRow:
        if updateRows[0] == 36:
            updateRow.deleteRow()

