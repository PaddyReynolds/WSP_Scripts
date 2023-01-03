#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     21/01/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import math

WorkGDD = r'C:\Users\UKPXR011\Desktop\Street_View\Full_Test\Output.gdb'
fc1 = r'C:\Users\UKPXR011\Desktop\Street_View\Bareing_Test\BaringTest.gdb\Parcels'
fc2 = r'C:\Users\UKPXR011\Desktop\Street_View\Bareing_Test\BaringTest.gdb\Points'


PointsFields = ['OwnershipReference','Shape@XY']
ownershipFields = ['OwnershipReference','Shape@XY','Bearing']



def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing



# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc2,PointsFields)}

with arcpy.da.UpdateCursor(fc1, ownershipFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[2] = calculate_initial_compass_bearing(valueDict[keyValue][0], updateRow[1])
            updateRows.updateRow(updateRow)


