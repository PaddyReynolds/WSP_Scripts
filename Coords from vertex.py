#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     06/11/2019
# Copyright:   (c) UKPXR011 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, math, datetime, numpy
from arcpy import env
print 'starting'
start = datetime.datetime.now() # for calculating time of process
coords = []
infc = r'C:\Users\UKPXR011\Desktop\Street_View\Scratch.gdb\SampleRoads'
pointFeat = 'C:\Users\UKPXR011\Desktop\Street_View\Scratch.gdb\RoadsL3L4_GeneratePointsAlon1'
# Enter for loop for each feature
#
for row in arcpy.da.SearchCursor(infc, ['OID@', 'SHAPE@']):
    partnum = 0
    # Step through each part of the feature
    for part in row[1]:

        # Step through each vertex in the feature
        for pnt in part:
                coords.append([int(pnt.X), int(pnt.Y)])

        partnum += 1

with arcpy.da.InsertCursor(pointFeat, ['SHAPE@XY']) as cursor:

    for i in coords:
        cursor.insertRow([i])

print 'Fuck i cant belive that worked'





