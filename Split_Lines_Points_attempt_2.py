__author__ = "John K. Tran"
__contact__ = "jtran20@masonlive.gmu.edu"
__version__ = "4.0"
__created__ = "7/16/15"
__credits__ = "http://gis.stackexchange.com/questions/154708/standalone-python-script-to-split-a-polyline-with-a-point-layer"

"""
'Cuts', 'splits' or 'dices' a polyline feature class using a point feature class.
The output schema (i.e. list of fields) will be blank, but you can use a spatial join
to repopulate the attributes to the output feature class.
"""

import arcpy
import os
import sys

arcpy.env.overwriteOutput = True
arcpy.SetProgressor("default", "Firing up script...")

linefc = r"C:\Users\UKPXR011\Desktop\Scratch\Strettview_Popup\Scratch.gdb\L3_L4_Roads_Dissolve" # Your polyline feature class
pointfc = r"C:\Users\UKPXR011\Documents\ArcGIS\Default.gdb\RoadsL3L4_GeneratePointsAlon" # Your point feature class
output = r"C:\Users\UKPXR011\Desktop\Scratch\Strettview_Popup\StreetView.gdb\NeverGoingToWork" # New output feature class.

spatialref1 = arcpy.Describe(pointfc).spatialReference
spatialref2 = arcpy.Describe(linefc).spatialReference
assert spatialref1.name == spatialref2.name, "Ensure both feature classes have the same projected coordinate system"

# If the Advanced license is available, just use the normal geoprocessing tools.
if arcpy.ProductInfo() in [u'ArcInfo', u'ArcServer']:
    arcpy.SetProgressorLabel("Splitting lines at points")
    arcpy.SplitLineAtPoint_management(linefc, pointfc, output, 1.0)
    arcpy.SetProgressorLabel("Deleting duplicate slices")
    outshapefieldname = arcpy.Describe(output).shapeFieldName
    arcpy.DeleteIdentical_management(output, [outshapefieldname])
    print ('Running 1')
    sys.exit(0)

# If not, proceed with script.
# Set up some preliminary variables to start.
arcpy.SetProgressorLabel("Gathering geometries")
points = [row[0] for row in arcpy.da.SearchCursor(pointfc, "SHAPE@")]
lines = [row[0] for row in arcpy.da.SearchCursor(linefc, "SHAPE@")]
cutlines = list()
iterations = 0
print ('Running ')

# Defining a function for the cut will let us reuse it again for subsequent cuts.
def CutLines():
    arcpy.SetProgressorLabel("Running cut: Iteration {0}".format(str(iterations)))
    for line in lines[:]:
        iscut = "Invalid"
        if line.length > 0.0: # Make sure it's not an empty geometry.
            iscut = "Not Cut"
            for point in points:
                if line.distanceTo(point) < 1.0: # Even "coincident" points can show up as spatially non-coincident in their floating-point XY values, so we set up a tolerance.
                    snappoint = line.snapToLine(point).firstPoint # To ensure coincidence, snap the point to the line before proceeding.
                    if not (snappoint.equals(line.lastPoint) and snappoint.equals(line.firstPoint)): # Make the sure the point isn't on a line endpoint, otherwise cutting will produce an empty geometry.
                        cutline1, cutline2 = line.cut(arcpy.Polyline(arcpy.Array([arcpy.Point(snappoint.X+10.0, snappoint.Y+10.0), arcpy.Point(snappoint.X-10.0, snappoint.Y-10.0)]), spatialref1)) # Cut the line.
                        if cutline1.length > 0.0 and cutline2.length > 0.0: # Make sure both descendents have non-zero geometry.
                            lines.insert(0, cutline1) # Feed the cut lines back into the "line" list to be recut.
                            lines.insert(0, cutline2) # The cut loop will only exit when all lines cannot be recut smaller and smaller (without producing zero-length geometries).
                            iscut = "Cut"
                            print ('Running 3')
        if iscut == "Not Cut":
            cutlines.insert(0, line)
        lines.remove(line)

# Perform the pseudo-recurive Cut loop until the polyline FC can't be cut further.
while lines:
    CutLines()
    iterations += 1
    if iterations > 500: # Fail-safe to stop an infinite loop if something goes wrong (or if more than 500 points intersect a single line).
        print ('Running 4')
        break

# Create the output feature class.
arcpy.SetProgressorLabel("Creating output feature class")
arcpy.CreateFeatureclass_management(os.path.dirname(output), os.path.basename(output), "POLYLINE", None, None, None, spatialref2)
print ('Running 5')

# Insert each cut line into the new feature class.
arcpy.SetProgressorLabel("Inserting cut lines")
with arcpy.da.InsertCursor(output, "SHAPE@") as insertcursor:
    for cutline in cutlines:
        insertcursor.insertRow((cutline,))
        print ('Running 6')

# Delete duplicates by comparing their geometry objects.
arcpy.SetProgressorLabel("Deleting duplicates")
crows = [row for row in arcpy.da.SearchCursor(output, ["OID@", "SHAPE@"])]
deleteOIDs = set() # Retain the OIDs for deletion, performed in the next cursor.
for drow in crows: # Compare each geometry to every other geometry in the output FC.
    dOID = drow[0]
    dgeom = drow[1]
    if dOID not in deleteOIDs:
        for srow in crows:
            sOID = srow[0]
            sgeom = srow[1]
            if sOID != dOID and sOID not in deleteOIDs: # Prevent redundant comparisons, only compare new combinations.
                dextent = dgeom.extent
                sextent = sgeom.extent
                if dextent.XMin == sextent.XMin and dextent.XMax == sextent.XMax and dextent.YMin == sextent.YMin and dextent.YMax == sextent.YMax: # See if their extents match first.
                    if dgeom.equals(sgeom): # Then see if they equal each other.
                        deleteOIDs.add(sOID) # If so, add the OID to the list of OIDs to delete.
with arcpy.da.UpdateCursor(output, "OID@") as deletecursor: # Delete the records here using your list of "DeleteOIDs".
    for delrow in deletecursor:
        delOID = delrow[0]
        if delOID in deleteOIDs:
            deletecursor.deleteRow()
            print ('Running 7')

# Clean up leftover variables.
namespace = dir()
for var in ["linecursor", "pointcursor", "insertcursor", "deletecursor"]:
    if var in namespace:
        exec "del " + var
        print ('Done')

arcpy.ResetProgressor()
