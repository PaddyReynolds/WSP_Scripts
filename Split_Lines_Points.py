import arcpy
arcpy.env.overwriteOutput = True

line_fc = r"C:\Users\UKPXR011\Desktop\Scratch\Strettview_Popup\StreetView.gdb\RoadsL3L4"
point_fc = r"C:\Users\UKPXR011\Documents\ArcGIS\Default.gdb\RoadsL3L4_GeneratePointsAlon"
point_fc_desc = arcpy.Describe(point_fc)
in_spatial_reference = point_fc_desc.spatialReference

#can use CopyFeatures to write the geometries to disk when troubleshooting
#buffered_point_fc = r"C:\GIS\Temp\test.gdb\PointsBuffered"
#intersected_line_fc = r"C:\GIS\Temp\test.gdb\LineIntersected"
#symmetrical_difference_line_fc = r"C:\GIS\Temp\test.gdb\LineIntersectedSymmDiff"
single_part_splitted_lines = r"C:\Users\UKPXR011\Desktop\Scratch\Strettview_Popup\Scratch.gdb\SplittedLines"
total_splitted_lines = r"C:\Users\UKPXR011\Desktop\Scratch\Strettview_Popup\Scratch.gdb\TotalSplittedLines"
total_splitted_lines_attributed = r"C:\Users\UKPXR011\Desktop\Scratch\Strettview_Popup\Scratch.gdb\TotalSplittedLinesAttributed"

arcpy.TruncateTable_management(total_splitted_lines)

#--- reference dictionaries ----------------#
points_id_geometry_dict = {} #{pointID: pointGeometry}
lines_id_geometry_dict = {} #{lineID: lineGeometry}

search_cursor = arcpy.da.SearchCursor(point_fc,["PointID","SHAPE@"])
for point_feature in search_cursor:
    points_id_geometry_dict[point_feature[0]] = point_feature[1]
del search_cursor

search_cursor = arcpy.da.SearchCursor(line_fc,["LineID","SHAPE@"])
for line_feature in search_cursor:
    lines_id_geometry_dict[line_feature[0]] = line_feature[1]
del search_cursor
#-------------------------------------------#

points_list =[]
lines_list = []

dictionary_lines_points = {} #{lineID: pointID} or {lineID: (pointID, pointID,...)}

point_cursor = arcpy.da.SearchCursor(point_fc,["SHAPE@","PointID"])
line_cursor = arcpy.da.SearchCursor(line_fc,["SHAPE@","LineID"])

for point in point_cursor:
    point_geom_and_id = [point[0],point[1]]
    points_list.append(point_geom_and_id)

for line in line_cursor:
    line_geom_and_id = [line[0],line[1]]
    lines_list.append(line_geom_and_id)

del point_cursor
del line_cursor

for line in lines_list:
    for point in points_list:
        if line[0].contains(point[0]): #finding what points are on what lines
            print "LineID:", line[1], "PointID:", point[1]
            if not line[1] in dictionary_lines_points: #handling situations when multiple points are on the same line
                dictionary_lines_points[line[1]] = point[1] #lineid is key, point ids is value (can be a tuple)
            else:
                dictionary_lines_points[line[1]] = (dictionary_lines_points[line[1]],point[1]) #making tuple for "" line: (point ids) ""

for key_line in dictionary_lines_points.keys(): #iterating each line in the line_fc
    pointID = dictionary_lines_points.get(key_line) #getting what PointID have match to lineID

    if not isinstance(pointID,tuple):
        input_point_geom_object = points_id_geometry_dict.get(pointID) #obtain point geometry based on pointID
        multipoints = input_point_geom_object
    else:
        merged_point_geometries = arcpy.Array() #constructing a multipoint (if multiple points are on the same line)
        for pointID_element in pointID:
            input_point_geom_object = points_id_geometry_dict.get(pointID_element)
            merged_point_geometries.add(input_point_geom_object.centroid) #creating array of points
            multipoints = arcpy.Multipoint(merged_point_geometries,in_spatial_reference)

    line_geometry_object = lines_id_geometry_dict.get(key_line) #obtain line geometry based on LineID

    buffered_point = multipoints.buffer(0.1) #same units as the geometry
    intersected_line = buffered_point.intersect(line_geometry_object,2) #2 - polyline returned
    symmetrical_difference_line = intersected_line.symmetricDifference(line_geometry_object)
    arcpy.MultipartToSinglepart_management(symmetrical_difference_line,single_part_splitted_lines)
    arcpy.Integrate_management(single_part_splitted_lines,"0.1 Meters")
    arcpy.Append_management(single_part_splitted_lines,total_splitted_lines,"NO_TEST")
    arcpy.Delete_management(single_part_splitted_lines)

    arcpy.SpatialJoin_analysis(target_features=total_splitted_lines,
                               join_features=line_fc,
                               out_feature_class=total_splitted_lines_attributed,
                               join_operation="JOIN_ONE_TO_ONE",join_type="KEEP_ALL",
                               match_option="INTERSECT",search_radius="#",distance_field_name="#")