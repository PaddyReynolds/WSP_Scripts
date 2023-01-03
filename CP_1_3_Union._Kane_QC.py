#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     20/12/2019
# Copyright:   (c) UKPXR011 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
import math
from datetime import *

arcpy.env.overwriteOutput = True

#Capture start time of script
start = datetime.now()
print 'Script: %s\n' % (start)

#Set global variables


#fc =r'C:\Users\UKPXR011\Desktop\Paddy_Work\GSSGISK-1324\PatCat_1.gdb\Limits'
fc1 = r'C:\Users\UKPXR011\Desktop\Paddy_Work\QC Work\CP3_1_Manchester\CP_Comparison.gdb\backupdata\LOP'
fc1u = r'C:\Users\UKPXR011\Desktop\Paddy_Work\QC Work\CP3_1_Manchester\CP_Comparison.gdb\backupdata\CP1_Inc_Tunnel_Section'
fc2u = r'C:\Users\UKPXR011\Desktop\Paddy_Work\QC Work\CP3_1_Manchester\CP_Comparison.gdb\backupdata\CP3_V4_Inc_Tunnel'


Ownership_Ref = []
inputGdb =r'C:\Users\UKPXR011\Desktop\Paddy_Work\QC Work\CP3_1_Manchester\CP_Comparison.gdb'
working = r'C:\Users\UKPXR011\Desktop\Paddy_Work\QC Work\CP3_1_Manchester\working.gdb'
output = r'C:\Users\UKPXR011\Desktop\Paddy_Work\QC Work\CP3_1_Manchester\output.gdb'
workspace = r'C:\Users\UKPXR011\Desktop\Paddy_Work\QC Work\CP3_1_Manchester'


#CP3Query = "LimitDescription = 'Consolidated Construction Boundary CP03'"
#CP1Query = "LimitDescription = 'Consolidated Construction Boundary CP01'"
CP1Dissolve = "LimitDescription"
#Extract CP3
#CP3 = arcpy.Select_analysis(fc,working + "\\CP3",CP3Query)

#Extract CP1
#CP1_Temp = arcpy.Select_analysis(fc,working + "\\CP1_temp",CP1Query)

#Dissolve CP1
#CP1 = arcpy.Dissolve_management(CP1_Temp,working + "\CP1",CP1Dissolve)

#union CP1 and cp3
Union=arcpy.Union_analysis ([fc1u, fc2u], working + "\\CPUnion")

#Select the unioned stuff

UnionSelect = arcpy.Select_analysis(Union,working +"\\CP1_3","FID_CP1_Inc_Tunnel_Section <> -1 AND FID_CP3_V4_Inc_Tunnel <> -1")
#intersect ownership and and CP1_3
intersectCP1_3_Ownership = arcpy.Intersect_analysis([UnionSelect,fc1], working +"\\CP1_3_Ownership", "ALL", "", "INPUT")

#Dissolve on ownership
CP1_Dissolve = arcpy.Dissolve_management(intersectCP1_3_Ownership,working + "\CP1_3_Ownership_Dissolve","OwnershipReferenceNumber")

#Write all ownership to a list
with arcpy.da.SearchCursor(CP1_Dissolve,['OwnershipReferenceNumber']) as cursor:
    for row in cursor:
        Ownership_Ref.append(row[0])

with open(os.path.join(workspace, "CP1_3_Ownership.txt"), "w") as f:
    for item in Ownership_Ref:
        f.write("%s\n" % item)

