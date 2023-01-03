#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     07/09/2021
# Copyright:   (c) UKPXR011 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os

inFC = r'\\DCEMA100APP53\Data\National_Polygon_Service\13_GSS\132_GIS\GIS_Data\Geodatabases\National_Polygon_Service_FullSupply.gdb\GEODATA\NPD_FullSupply'

Output_Folder = r'C:\Users\UKPXR011\Desktop\Scripts\NPS_Extract'
Output_GDB = Output_Folder + "\\" + 'NPS_Extract.gdb'
outFC = Output_GDB+'\Titles_19082022'

where_clause = """ "TITLE_NO" IN ('CH714962',
'GM864743',
'MAN147937',
'MAN166763',
'MAN267765',
'MAN269412',
'MAN269416',
'MAN269418',
'MAN269588',
'MAN269594',
'MAN269599',
'MAN269601',
'MAN269602',
'MAN269606',
'MAN269608',
'MAN269611',
'MAN278964',
'MAN280771',
'MAN285800',
'MAN290942',
'MAN294517',
'MAN296416',
'MAN296525',
'MAN298293',
'MAN302444',
'MAN305059',
'MAN305408',
'MAN307107',
'MAN307712',
'MAN311788',
'MAN334164',
'MAN334725',
'MAN338504',
'MAN338505',
'MAN343435',
'MAN348435',
'MAN348650',
'MAN350310',
'MAN351293',
'MAN353143',
'MAN357044',
'MAN357382',
'MAN361321',
'MAN372777',
'MAN374572',
'MAN374573',
'MAN374903',
'MAN375291',
'MAN375445',
'MAN376013',
'MAN376668',
'MAN379258',
'MAN385624',
'MAN388511',
'MAN388673',
'MAN394405')"""

arcpy.env.workspace = Output_GDB
arcpy.env.overwriteOutput = True


if os.path.exists(Output_GDB):

    print 'GDB Already Exists'

    if arcpy.Exists(outFC):
        arcpy.Delete_management(outFC)
        print 'Feature Overwritten'

else:
     arcpy.management.CreateFileGDB(Output_Folder, 'NPS_Extract')


arcpy.Select_analysis(inFC, outFC, where_clause)


print "Done"
