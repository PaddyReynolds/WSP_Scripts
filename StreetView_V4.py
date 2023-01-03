# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# StreetView_V4.py
# Created on: 2019-09-11 10:11:25.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: StreetView_V4 <Create_Folder_for_data> <Roads> <Ownership>
# Description:
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Script arguments
Create_Folder_for_data = arcpy.GetParameterAsText(0)
if Create_Folder_for_data == '#' or not Create_Folder_for_data:
    Create_Folder_for_data = "C:\\Users\\UKPXR011\\Desktop\\Scratch\\Strettview_Popup\\Model" # provide a default value if unspecified

Roads = arcpy.GetParameterAsText(1)
if Roads == '#' or not Roads:
    Roads = "C:\\Users\\UKPXR011\\Desktop\\Scratch\\Strettview_Popup\\Sample.gdb\\Roads" # provide a default value if unspecified

Ownership = arcpy.GetParameterAsText(2)
if Ownership == '#' or not Ownership:
    Ownership = "C:\\Users\\UKPXR011\\Desktop\\Scratch\\Strettview_Popup\\Sample.gdb\\Ownership" # provide a default value if unspecified

# Local variables:
Ownership_Layer = "Ownership_Layer"
Ownership_Layer__2_ = Ownership_Layer
Ownership_Layer__5_ = Ownership_Layer__2_
Folder_Storing_All_Data = Create_Folder_for_data
Scratch = Folder_Storing_All_Data
Roads_Dissolved = "%Scratch%\\Roads_Dissolved"
Roads_Points = "%Scratch%\\Roads_Points"
Roads_Points__2_ = Roads_Points
Roads_Points__3_ = Roads_Points__2_
Roads_Points_Layer = "Roads_Points_Layer"
Ownership_Layer__6_ = Roads_Points_Layer
Ownership_SpatialJoin = "%Scratch%/Ownership_SpatialJoin"
JoinPoints = "%Scratch%\\JoinPoints"
Roads_Points_Layer__2_ = Ownership_Layer__6_
Roads_Points_Layer__3_ = Roads_Points_Layer__2_
Ownership_Layer__3_ = Ownership_Layer__5_
Output_Feature_Class = ""

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(Ownership, Ownership_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;OwnershipReferenceNumber OwnershipReferenceNumber VISIBLE NONE;GlobalID GlobalID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;SHAPE_Length SHAPE_Length VISIBLE NONE;SHAPE_Area SHAPE_Area VISIBLE NONE;lat lat VISIBLE NONE;Lng Lng VISIBLE NONE;StreetViewURL StreetViewURL VISIBLE NONE;Street_View_URL Street_View_URL VISIBLE NONE")

# Process: Add Field (5)
arcpy.AddField_management(Ownership_Layer, "Street_View_URL", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Create Folder
arcpy.CreateFolder_management(Create_Folder_for_data, "Street_View5")

# Process: Create File GDB
arcpy.CreateFileGDB_management(Folder_Storing_All_Data, "Scratch", "CURRENT")

# Process: Dissolve
arcpy.Dissolve_management(Roads, Roads_Dissolved, "", "", "MULTI_PART", "DISSOLVE_LINES")

# Process: Generate Points Along Lines
arcpy.GeneratePointsAlongLines_management(Roads_Dissolved, Roads_Points, "DISTANCE", "10 Meters", "", "")

# Process: Add Field
arcpy.AddField_management(Roads_Points, "X", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (2)
arcpy.AddField_management(Roads_Points__2_, "Y", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Make Feature Layer (2)
arcpy.MakeFeatureLayer_management(Roads_Points__3_, Roads_Points_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE;X X VISIBLE NONE;Y Y VISIBLE NONE")

# Process: Spatial Join
arcpy.SpatialJoin_analysis(Ownership_Layer__2_, Roads_Points_Layer, Ownership_SpatialJoin, "JOIN_ONE_TO_ONE", "KEEP_ALL", "OwnershipReferenceNumber \"Ownership Reference Number\" true true false 4 Long 0 0 ,First,#,Ownership_Layer,OwnershipReferenceNumber,-1,-1;GlobalID \"GlobalID\" false false true 38 GlobalID 0 0 ,First,#,Ownership_Layer,GlobalID,-1,-1;SHAPE_Length \"SHAPE_Length\" false true true 8 Double 0 0 ,First,#,Ownership_Layer,SHAPE_Length,-1,-1;SHAPE_Area \"SHAPE_Area\" false true true 8 Double 0 0 ,First,#,Ownership_Layer,SHAPE_Area,-1,-1;lat \"lat\" true true false 8 Double 0 0 ,First,#,Ownership_Layer,lat,-1,-1;Lng \"Lng\" true true false 8 Double 0 0 ,First,#,Ownership_Layer,Lng,-1,-1;StreetViewURL \"StreetViewURL\" true true false 100 Text 0 0 ,First,#,Ownership_Layer,StreetViewURL,-1,-1;Street_View_URL \"Street_View_URL\" true true false 100 Text 0 0 ,First,#,Ownership_Layer,Street_View_URL,-1,-1;ORIG_FID \"ORIG_FID\" true true false 7077996 Short 6881397 7143470 ,First,#,Roads_Points_Layer,ORIG_FID,-1,-1;X \"X\" true true false 0 Double 0 0 ,First,#,Roads_Points_Layer,X,-1,-1;Y \"Y\" true true false 0 Double 0 0 ,First,#,Roads_Points_Layer,Y,-1,-1", "CLOSEST", "50 Meters", "")

# Process: Select
arcpy.Select_analysis(Ownership_SpatialJoin, JoinPoints, "Ownership_SpatialJoin.Join_Count >= 1")

# Process: Add Join (2)
arcpy.AddJoin_management(Roads_Points_Layer, "ORIG_FID", JoinPoints, "ORIG_FID", "KEEP_ALL")

# Process: Calculate Field
arcpy.CalculateField_management(Ownership_Layer__6_, "Roads_Points.X", "arcpy.PointGeometry(!Shape!.firstPoint,!Shape!.spatialReference).projectAs(arcpy.SpatialReference(3857)).firstPoint.X", "PYTHON_9.3", "")

# Process: Calculate Field (2)
arcpy.CalculateField_management(Roads_Points_Layer__2_, "Roads_Points.Y", "arcpy.PointGeometry(!Shape!.firstPoint,!Shape!.spatialReference).projectAs(arcpy.SpatialReference(3857)).firstPoint.Y", "PYTHON_9.3", "")

# Process: Add Join
arcpy.AddJoin_management(Ownership_Layer__2_, "Ownership_SpatialJoin.Ownership_OwnershipReferenceNumber", Roads_Points_Layer__3_, "Ownership.OwnershipReferenceNumber", "KEEP_ALL")

# Process: Calculate Field (5)
arcpy.CalculateField_management(Ownership_Layer__5_, "Street_View_URL", "\"http://maps.google.com/maps?q=&layer=c&cbll=\"+String( !Roads_Points.Roads_Points.X! )+\",\"+String( !Roads_Points.Roads_Points.Y! )+\"&cbp=11,0,0,0,0\"", "PYTHON_9.3", "")

# Process: Copy Features
arcpy.CopyFeatures_management("", Output_Feature_Class, "", "0", "0", "0")

