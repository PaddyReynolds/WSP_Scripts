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

arcpy.env.overwriteOutput = True

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

#Roads
fc1 = r'C:\Users\UKPXR011\Desktop\Street_View\Scratch.gdb\SampleRoads'
#Points
fc2 = 'C:\Users\UKPXR011\Desktop\Street_View\Scratch.gdb\Road_Point_Test'
#Lop
fc3 = 'C:\Users\UKPXR011\Desktop\Street_View\Scratch.gdb\LOP'
#LOP Join
fc4 = WorkGDD + '\LOPSpatialJoin'
#Projected Roads
fc5 = WorkGDD + '\Projected_Roads_points'
#Projected LOp
fc6 = WorkGDD + '\Projected_LOP'

StreetViewField = "Street_View_URL"
OwnershipRef = 'OwnershipReferenceNumber'
JoinDist = 'JoinDistance'
X_Field = 'X_Point'
Y_Field = 'Y_Point'
coords = []

#Fields to populate X and Y in Points
updateFieldsListX_Y = [X_Field, Y_Field, 'SHAPE@X', 'SHAPE@Y']
updateFieldsListX_Y2 = [X_Field, Y_Field, 'OID@', 'SHAPE@']

#Fields for making the streetview URL in the joined LOP's
updateFieldsListSpatialJoin = [X_Field, Y_Field,StreetViewField,JoinDist]

#Transfereing Streetview URL to Ownership Polygons
ownershipFields = [OwnershipRef,StreetViewField]


#Add an X and a Y field
arcpy.AddField_management(fc2, X_Field, "DOUBLE","","","", "", "", "", "")
arcpy.AddField_management(fc2, Y_Field, "DOUBLE","","","", "", "", "", "")




arcpy.Project_management(fc1, fc5, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "OSGB_1936_To_WGS_1984_Petroleum", "PROJCS['British_National_Grid',GEOGCS['GCS_OSGB_1936',DATUM['D_OSGB_1936',SPHEROID['Airy_1830',6377563.396,299.3249646]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',400000.0],PARAMETER['False_Northing',-100000.0],PARAMETER['Central_Meridian',-2.0],PARAMETER['Scale_Factor',0.9996012717],PARAMETER['Latitude_Of_Origin',49.0],UNIT['Meter',1.0]]", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
#Project LOP
arcpy.Project_management(fc3, fc4, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "OSGB_1936_To_WGS_1984_Petroleum", "PROJCS['British_National_Grid',GEOGCS['GCS_OSGB_1936',DATUM['D_OSGB_1936',SPHEROID['Airy_1830',6377563.396,299.3249646]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',400000.0],PARAMETER['False_Northing',-100000.0],PARAMETER['Central_Meridian',-2.0],PARAMETER['Scale_Factor',0.9996012717],PARAMETER['Latitude_Of_Origin',49.0],UNIT['Meter',1.0]]", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")

for row in arcpy.da.SearchCursor(fc5, ['OID@', 'SHAPE@']):
    partnum = 0
    # Step through each part of the feature
    for part in row[1]:

        # Step through each vertex in the feature
        for pnt in part:
                coords.append([int(pnt.X), int(pnt.Y)])

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

    cursor.updateRow(row)

del row, cursor

print "X and Y Coordinates Added"


print "Spatial Joining"

arcpy.SpatialJoin_analysis(fc3, fc2, fc4,"","KEEP_ALL","","CLOSEST","50","JoinDist")

print "Spatial Join Complete"


with arcpy.da.UpdateCursor(fc4, updateFieldsListSpatialJoin) as updateRow:

    for row in updateRow:

        if row[3] == None :

            row[2] = "Road Too Far for Streeview"
            updateRow.updateRow(row)


        else:
            #Build the Hyoerlink
            row[2] = "http://maps.google.com/maps?q=&layer=c&cbll="+ str(row[1])+","+str(row[0])+"&cbp=11,0,0,0,0"
            print row[2]
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




