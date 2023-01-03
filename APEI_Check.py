#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     23/06/2022
# Copyright:   (c) UKPXR011 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

fc1 = r'C:\Users\UKPXR011\Desktop\Current Work\2b\APEI\EW\2C864-MCL-GI-GDD-M000-000032_P09\2C864-MCL-GI-GDD-M000-000032_P09\Y22W25.gdb\PRP_MCL_2C864_AffectedPartiesEngagementIndex_Tbl'


seen = set()
dupes = []
unq = set()
fields = ['LR_Title' ,'LandOwnNo' ,'PIDNo']
'''
with arcpy.da.SearchCursor(fc1, ['HS2_SupDoc']) as cursor:
    for row in cursor:
        if row in seen:
            dupes.append(row)
        else:
            seen.add(row)

print len(dupes)
'''
dupes = []

with arcpy.da.SearchCursor(fc1, fields) as cursor:
    for row in cursor:
        x = str(row[0] + row[1] + row[2])
        if x in unq:
            dupes.append(x)
        else:
                unq.add(x)

print len(dupes), len(unq)






