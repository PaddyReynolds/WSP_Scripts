#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      UKPXR011
#
# Created:     05/11/2019
# Copyright:   (c) UKPXR011 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, math, datetime, numpy, os
from arcpy import env

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        ? = atan2(sin(?long).cos(lat2),
                  cos(lat1).sin(lat2) ? sin(lat1).cos(lat2).cos(?long))
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
    # from -180? to + 180? which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


arcpy.env.overwriteOutput = True
'''
#Create local GDB & work folders
arcpy.AddMessage("Creating Local Copy")
desktopPath = os.environ.get( "USERPROFILE" ) + "\\Desktop"
TempFolder = desktopPath + "\\StreetView_URL_Scratch"
if os.path.exists(TempFolder) == False:
    os.makedirs(TempFolder)
ScratchGDD = "Scratch"
WorkGDD = TempFolder + "\\" + ScratchGDD + ".gdb"
if os.path.exists(WorkGDD) == False:
   arcpy.CreateFileGDB_management(TempFolder,ScratchGDD)
'''
WorkGDD = r'C:\Users\UKPXR011\Desktop\Scratch\Street_View\Scratch.gdb'
#Roads
fc1 = r'C:\Users\UKPXR011\Desktop\Scratch\Street_View\Scratch.gdb\Roads'
#Points
fc2 = r'C:\Users\UKPXR011\Desktop\Scratch\Street_View\Scratch.gdb\Points'
#Lop
fc3 = r'C:\Users\UKPXR011\Desktop\Scratch\Street_View\Street_View.gdb\STATUTORY_PROCESSES\LandOwnershipParcels'
#LOP Join
fc4 = WorkGDD + '\LOPSpatialJoin'
#Projected Roads
fc5 = WorkGDD + '\Projected_Roads_points'
#Projected LOp
fc6 = WorkGDD + '\Projected_LOP'

StreetViewField = "StreetView_URL"
OwnershipRef = 'OwnershipReferenceNumber'
JoinDist = 'JoinDist'
X_Field = 'X_Point'
Y_Field = 'Y_Point'
XY_Field = 'XY'
coords = []

#Fields to populate X and Y in Points
updateFieldsListX_Y = [X_Field, Y_Field, 'SHAPE@X', 'SHAPE@Y',XY_Field,'SHAPE@XY']
updateFieldsListX_Y2 = [X_Field, Y_Field, 'OID@', 'SHAPE@']

#Fields for making the streetview URL in the joined LOP's
updateFieldsListSpatialJoin = [X_Field, Y_Field,XY_Field,'SHAPE@XY',StreetViewField,JoinDist]

#Transfereing Streetview URL to Ownership Polygons
ownershipFields = [OwnershipRef,StreetViewField]


#Add an X and a Y field
arcpy.AddField_management(fc2, X_Field, "FLOAT","","","", "", "", "", "")
arcpy.AddField_management(fc2, Y_Field, "FLOAT","","","", "", "", "", "")
arcpy.AddField_management(fc2, XY_Field, "Text","","","", "", "", "", "")

arcpy.Project_management(fc1, fc5, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "OSGB_1936_To_WGS_1984_Petroleum", "PROJCS['British_National_Grid',GEOGCS['GCS_OSGB_1936',DATUM['D_OSGB_1936',SPHEROID['Airy_1830',6377563.396,299.3249646]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',400000.0],PARAMETER['False_Northing',-100000.0],PARAMETER['Central_Meridian',-2.0],PARAMETER['Scale_Factor',0.9996012717],PARAMETER['Latitude_Of_Origin',49.0],UNIT['Meter',1.0]]", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
#Project LOP
arcpy.Project_management(fc3, fc6, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "OSGB_1936_To_WGS_1984_Petroleum", "PROJCS['British_National_Grid',GEOGCS['GCS_OSGB_1936',DATUM['D_OSGB_1936',SPHEROID['Airy_1830',6377563.396,299.3249646]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',400000.0],PARAMETER['False_Northing',-100000.0],PARAMETER['Central_Meridian',-2.0],PARAMETER['Scale_Factor',0.9996012717],PARAMETER['Latitude_Of_Origin',49.0],UNIT['Meter',1.0]]", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")

for row in arcpy.da.SearchCursor(fc5, ['OID@', 'SHAPE@']):
    partnum = 0
    # Step through each part of the feature
    for part in row[1]:

        # Step through each vertex in the feature
        for pnt in part:
                coords.append([float(pnt.X), float(pnt.Y)])

        partnum += 1

with arcpy.da.InsertCursor(fc2, ['SHAPE@XY']) as cursor:

    for i in coords:

        cursor.insertRow([i])

print 'Points Created'


#Get the X&Y into a field to use in the join
cursor = arcpy.da.UpdateCursor(fc2,updateFieldsListX_Y)
for row in cursor:
    row[0] = row[2]
    #Populate the Yfield with the Y geometry
    row[1] = row[3]
    row[4] = row[5]

    cursor.updateRow(row)

del row, cursor

print "X and Y Coordinates Added"


print "Spatial Joining"

arcpy.SpatialJoin_analysis(fc3, fc2, fc4,"","KEEP_ALL","","CLOSEST_GEODESIC","50","JoinDist")

print "Spatial Join Complete"


with arcpy.da.UpdateCursor(fc4, updateFieldsListSpatialJoin) as updateRow:

    for row in updateRow:

        if row[3] == -1 :
            row[2] = "Road Too Far for Streeview"
            print row[2]
            updateRow.updateRow(row)


        else:
            #Build the Hyoerlink
            row[4] = "http://maps.google.com/maps?q=&layer=c&cbll="+ str(row[1])+","+str(row[0])+"&heading="+str(calculate_initial_compass_bearing(row[2], row[3]))+"&cbp=11,0,0,0,0"
            updateRow.updateRow(row)

# Use list comprehension to build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc4,ownershipFields)}

with arcpy.da.UpdateCursor(fc3, ownershipFields) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
         # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
             # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[1] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

del valueDict

print "done"




