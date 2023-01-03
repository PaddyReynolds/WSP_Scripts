#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     24/10/2022
# Copyright:   (c) UKPXR011 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, os

fc1 =r'C:\Users\UKPXR011\Desktop\Current Work\2b\Postcodes\GIS_Data_Request_4243__20220412\GIS_Data_Request_4243\Data.gdb\ADM_ORDSU_PostcodePolygonsWithVerticalStreets_Ply'
fc2 =r'C:\Users\UKPXR011\Desktop\Current Work\2b\Postcodes\GIS_Data_Request_4243__20220412\GIS_Data_Request_4243\Data.gdb\ADM_ORDSU_PostcodeVerticalStreets'
File_Location =r'C:\\Users\\UKPXR011\\Desktop\\Current Work\\2b\\Postcodes\\AP2'
AOI = r'C:\Users\UKPXR011\Desktop\Current Work\2b\Postcodes\AP2\Scratch.gdb\AOI'

GDB = r'C:\\Users\\UKPXR011\\Desktop\\Current Work\\2b\\Postcodes\\AP2\\Scratch.gdb'

arcpy.env.workspace = GDB
arcpy.env.overwriteOutput = True


#Intersect
IntersectOutput = str(GDB+"\\AOI_Intersect")
print IntersectOutput
arcpy.analysis.Intersect([fc1, AOI], IntersectOutput)

#Dissolve
DissolveOutput =str(GDB+"\\PostCodeDissolve")
arcpy.management.Dissolve(IntersectOutput, DissolveOutput,['POSTCODE','VS_POSTCODE'])
#Export Option 1 to excel
PostCodes = []
PostCodes_1 = []
VPostCodes_1 =[]
sourceFieldsList = ['VS_REF','POSTCODE']

valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc2, sourceFieldsList)}

with arcpy.da.SearchCursor(DissolveOutput, ['POSTCODE','VS_POSTCODE']) as Cursor:
    for row in Cursor:
        PostCodes_1.append(row[0])
        if row[1] is not None:
            keyValue = row[1]
            if keyValue in valueDict:
                VPostCodes_1.append(valueDict[keyValue][0])


del Cursor

PostCodes.extend(PostCodes_1)
PostCodes.extend(VPostCodes_1)
PostCodes = list(dict.fromkeys(PostCodes))
7
CSV_Post_Codes_1 = os.path.join(File_Location, "PostCodes_1.csv")

if os.path.exists(CSV_Post_Codes_1):
    os.remove(CSV_Post_Codes_1)

with open(os.path.join(CSV_Post_Codes_1), "w") as f:
    for item in PostCodes:
        f.write("%s\n" % item)

print "Done"


#Export Option 2

arcpy.MakeFeatureLayer_management(fc1, "fc1_Lyr")
arcpy.MakeFeatureLayer_management(AOI, "AOI_Lyr")
PostCodes = arcpy.SelectLayerByLocation_management("fc1_Lyr", 'INTERSECT', "AOI_lyr")
VerticalPostCodes = arcpy.SelectLayerByLocation_management("fc1_Lyr", 'INTERSECT', PostCodes)


PostCodes_2 = []
VPostCodes_2=[]
with arcpy.da.SearchCursor(VerticalPostCodes, ['POSTCODE','VS_POSTCODE']) as Cursor:
    for row in Cursor:
        if row[1] is not None:
            keyValue = row[1]
            if keyValue in valueDict:
                VPostCodes_2.append(valueDict[keyValue][0])




PostCodes_2.extend(PostCodes_1)
PostCodes_2.extend(VPostCodes_2)
PostCodes_2 = list(dict.fromkeys(PostCodes_2))

CSV_Post_Codes_2 = os.path.join(File_Location, "PostCodes_2.csv")

if os.path.exists(CSV_Post_Codes_2):
    os.remove(CSV_Post_Codes_2)

with open(os.path.join(CSV_Post_Codes_2), "w") as f:
    for item in PostCodes_2:
        f.write("%s\n" % item)












