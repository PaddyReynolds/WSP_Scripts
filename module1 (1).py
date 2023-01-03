#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     03/02/2022
# Copyright:   (c) UKPXR011 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy



fc1 = r'C:\Users\UKPXR011\Desktop\Scripts\2a_GDD\Multipart Finder\Scratch.gdb\Test'

SearchRows = ["Name","SHAPE@XY"]

with arcpy.da.SearchCursor(fc1,['OID@','SHAPE@']) as cursor:
    for row in cursor:
        if row[1].isMultipart is True:
            print 'Yes'

        else:
            print 'No'