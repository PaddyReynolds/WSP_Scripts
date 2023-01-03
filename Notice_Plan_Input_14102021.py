#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     17/05/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import collections
import arcpy
import locale
locale.setlocale(locale.LC_ALL, '')

#Create Table for input
excel = r'C:\Users\UKPXR011\Desktop\Scripts\Noitce Plans\A203_003.xlsx'
LAPS = r'C:\Users\UKPXR011\Desktop\Scripts\Noitce Plans\Input_Data.gdb\LAPS'
OutputLocation = r'C:\Users\UKPXR011\Desktop\Scripts\Noitce Plans\Scratch.gdb'
OutputName = "Notice_Plan_Input"
Table_Name = "Input_Table"
QueryTable = "QueryTable"
Districts = r'C:\Users\UKPXR011\Desktop\Scripts\Noitce Plans\Scratch.gdb\Districts_2a'

arcpy.env.workspace = OutputLocation
arcpy.env.overwriteOutput = True
#
fc1 = OutputLocation + "\\" + Table_Name
fc2 = OutputLocation + "\\" + OutputName
fc3 = OutputLocation +'\\' + "LAPS"
fc4 = OutputLocation +'\\' + "Notice_Plan_Input_Feature"
fc5 = OutputLocation +'\\' +"Notice_Plan_Input_Feature_District_1"
fc5_1 = OutputLocation +'\\' +"Notice_Plan_Input_Feature_District_2"
fc5_2 = OutputLocation +'\\' +"Notice_Plan_Input_Feature_District_3"
fc6 = OutputLocation+'\\' + "Extents_Temp"
field1 = "Notice_Number"
field2 = "LAP_IDs"
field3 = "Notice_Number"
field4 = "LAP_IDs"

#convert table to excel
arcpy.conversion.ExcelToTable(excel,fc1)
#arcpy.env.worskspace = OutputLocation


#Create an empty table and add fields to hold the LAP_ID and Notice number
arcpy.CreateTable_management(OutputLocation,OutputName)
arcpy.AddField_management(fc2,field3,"TEXT",field_length=150)
arcpy.AddField_management(fc2,field4,"TEXT",field_length=150)

#Start Editing the GDB with the table in it
edit = arcpy.da.Editor(OutputLocation)
edit.startEditing(False, True)
edit.startOperation()

#Make a search cursor for the table converted from excel
searchC =  arcpy.da.SearchCursor(fc1, (field2,field1))
#Make an insert cursor for the new table created with the two fields added
insertC = arcpy.da.InsertCursor(fc2, (field3,field4))

#Loop through the search cursor, unconcatenate the LAP's which are delimited by a ; and insert a row into the new table for every lap recording the LAPid AND Notice Number
for row in searchC:
    A = [x.split(";") for x in row[:-1] ]
    Ref2 = row[1]
    print Ref2
    for i in A[0]:
        listA = [str(Ref2),str(i)]
        insertC.insertRow(listA)

del searchC, insertC

edit.stopOperation()
edit.stopEditing(True)
# stop edditing

#Add the remaining fields required for the Input feature
fields = [
    "Party_ID","Party_Org_Name","Acquisition_Method","Land_Request_Type","LAA_Code"
]

#Loop through list of fields and add each one
for field in fields:
    arcpy.AddField_management(fc2,field,"TEXT",field_length=150)

#remove spaces from LAPID column
with arcpy.da.UpdateCursor(fc2,field4) as cursor:
    for row in cursor:
        row=[i.strip() if i is not None else None for i in row]
        cursor.updateRow(row)

del cursor

#Add Notice number to list of fields to allow it to be populated in the update cursor
updateFields = ["Notice_Number"] + fields

#Make a dictionary of the converted excel to table
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc1,updateFields)}

#Open an update cursor for the new table which has been unconcatnated and update the relevant rows
with arcpy.da.UpdateCursor(fc2, updateFields) as updateRows:

        for updateRow in updateRows:
            # store the Join value of the row being updated in a keyValue variable
            keyValue = updateRow[0]
             # verify that the keyValue is in the Dictionary
            if keyValue in valueDict:

                updateRow[1] = valueDict[keyValue][0]
                updateRow[2] = valueDict[keyValue][1]
                updateRow[3] = valueDict[keyValue][2]
                updateRow[4] = valueDict[keyValue][3]
                updateRow[5] = valueDict[keyValue][4]

                updateRows.updateRow(updateRow)

del updateRows


#arcpy.analysis.Select(LAPS, fc3,)

#Set a veriable for the query table input
query_Table_Input = fc2 +";"+ fc3

#Make a query table adding the geometry for each LAP to each row
arcpy.MakeQueryTable_management(query_Table_Input, QueryTable, "USE_KEY_FIELDS", "", "LAPS.Shape #;Notice_Plan_Input.Notice_Number #;Notice_Plan_Input.LAP_IDs #;Party_ID #;Notice_Plan_Input.Party_Org_Name #;Notice_Plan_Input.Acquisition_Method #;Notice_Plan_Input.Land_Request_Type #;Notice_Plan_Input.LAA_Code #", "LAPS.LAPID = Notice_Plan_Input.LAP_IDs")

#extract the query table
arcpy.analysis.Select(QueryTable, fc4)

# intersect lAPS with area, dissolve on all fields and area,
IntersectFeatures = [fc4,Districts]
arcpy.Intersect_analysis(IntersectFeatures,fc5)

dissolve_fields = ["Notice_Plan_Input_Notice_Number","NAME"]

arcpy.Dissolve_management(fc5,fc5_1,dissolve_fields)

#Check to see if any Notices have more than one district, if they do then concatenate, if they dont then move on

templist = []

with arcpy.da.SearchCursor(fc5_1,dissolve_fields) as searchRows:
    for row in searchRows:
        templist.append(row[0])

del searchRows
print templist


NoticeSet = set([x for x in templist if templist.count(x) > 1])
print NoticeSet

#if this is True then Concatenate and dissolve again
if len(NoticeSet) != 0:
    arcpy.AddField_management(fc5_1,"District_Concat","TEXT",field_length=150)


dissovle_Fields = ["Notice_Plan_Input_Notice_Number","Party_ID","Notice_Plan_Input_Party_Org_Name","Notice_Plan_Input_Acquisition_Method","Notice_Plan_Input_Land_Request_Type","Notice_Plan_Input_LAA_Code"]
arcpy.Dissolve_management(fc4,fc6,dissovle_Fields)
arcpy.AddField_management(fc6,"Scale","LONG")



with arcpy.da.UpdateCursor(fc6, ["SHAPE@", "Notice_Plan_Input_Notice_Number", "Scale"]) as updateRows:

    for updateRow in updateRows:
        extent = updateRow[0].extent
        #LAA_ID = ("{0}".format(row[1]))
            # Create a polygon geometry
        array = arcpy.Array([arcpy.Point(extent.XMin, extent.YMin), arcpy.Point(extent.XMax, extent.YMin),
                                 arcpy.Point(extent.XMax, extent.YMax), arcpy.Point(extent.XMin, extent.YMax)])
        polygon = arcpy.Polygon(array)
        polygon_area = float(polygon.area)
        if polygon_area < 100000.00: #140767.95:
            Intial_Scale = '1250'
            updateRow[2] = Intial_Scale
        elif 100000.01 < polygon_area < 350000.00:
            Intial_Scale = '2500'
            updateRow[2] = Intial_Scale
        elif 350000.01 < polygon_area < 1800000.00:
            Intial_Scale = '5000'
            updateRow[2] = Intial_Scale
        elif 1800000.01 < polygon_area < 4500000.00:
            Intial_Scale = '7500'
            updateRow[2] = Intial_Scale
        else:
            Intial_Scale = '10000'
            updateRow[2] = Intial_Scale

        updateRows.updateRow(updateRow)

del updateRows


#update cursor all the relevant fields

# append into new feature classes

#Done

