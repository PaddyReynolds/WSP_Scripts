#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     12/02/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# import libraries
import arcpy

# set input/output parameters
polyFC = r'C:\Users\UKPXR011\Desktop\Scratch\Scratch.gdb\Line_Test' # input polygons
outParallel = r'C:\Users\UKPXR011\Desktop\Scratch\Scratch.gdb\Line' # output parallel lines
lineSpacing = 1 # line spacing
buffDist = 0 # inner buffer distance

# parse numbers from parameters
lineSpaceNum = 1
buffNum = 0

# establish spatial reference
desc = arcpy.Describe(polyFC)
SR = desc.spatialReference

# set overwrite environment
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = SR

parallels = []
# loop through each input shape
for row in arcpy.da.SearchCursor(polyFC, ["SHAPE@"], spatial_reference=SR):

  # create inner buffer
  polyBuff = row[0].buffer(buffNum * -1)

  # create hull rectangle to establish a rotated area of interest
  coordSplit = row[0].hullRectangle.split(' ')

  # collect corner coordinates
  coordList = arcpy.Array([arcpy.Point(coordSplit[0],coordSplit[1]),arcpy.Point(coordSplit[2],coordSplit[3]),arcpy.Point(coordSplit[4],coordSplit[5]),arcpy.Point(coordSplit[6],coordSplit[7]),arcpy.Point(coordSplit[0],coordSplit[1])])

  # create lines from hull rectangle
  currentLines = []
  for pointNum in range(0,4):
      arcpy.Array([coordList.getObject(pointNum),coordList.getObject(pointNum+1)])
      hullRecLine = arcpy.Polyline(arcpy.Array([coordList.getObject(pointNum),coordList.getObject(pointNum+1)]))
      currentLines.append(hullRecLine)

      # compare first and second line to determine if first line is short or long
  firstLong = 0
  if currentLines[0].length > currentLines[1].length:
    firstLong = 1

      # calculate number of points needed along short axis
  numPoints = int(math.floor(currentLines[firstLong].length/lineSpaceNum))

        # create and join points to create parallel lines
  for point in range(1,numPoints+1):
            shortPoint1 = currentLines[firstLong].positionAlongLine(lineSpaceNum*point)
            shortPoint2 = currentLines[firstLong + 2].positionAlongLine(currentLines[firstLong + 2].length - (lineSpaceNum*point))
            parallel = arcpy.Polyline(arcpy.Array([shortPoint1.centroid,shortPoint2.centroid]), SR)

          # intersect parallel lines with buffer
            parallelBuff = parallel.intersect(polyBuff,2)
            parallels.append(parallelBuff)

# write geometries to disk
print parallels
arcpy.CopyFeatures_management(parallels, outParallel)

# add to map
#mxd = arcpy.mapping.MapDocument("CURRENT")
#dataFrame = arcpy.mapping.ListDataFrames(mxd, "*")[0]
#addLayer = arcpy.mapping.Layer(outParallel)
#arcpy.mapping.AddLayer(dataFrame, addLayer)

del row