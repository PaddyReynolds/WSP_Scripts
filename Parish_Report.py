#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     08/01/2020
# Copyright:   (c) UKPXR011 2020
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

#CSet the workspace
#desktopPath = r'C:\Users\UKPXR011\Desktop\Scratch\Historical_GDB'

#set the environment
#SDE_Geodatabase = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde"
#arcpy.env.workspace = SDE_Geodatabase

fc = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde\STATUTORY_PROCESSES\LandOwnershipParcels"
#fc =  r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Data.gdb\Ownership'
fc1 = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde\STATUTORY_PROCESSES\Limits"
#fc1 = r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Data.gdb\Limits'
fc2 = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde\HS2phase2B_WSP.GSS.HS2\HS2phase2B_WSP.GSS.Parish"
#fc2 = r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Data.gdb\Parish'
CP3Query = "LimitDescription = 'Consolidated Construction Boundary CP03'"
L3Query = "LimitDescription = 'L3 Landgroup'"
MMLQuery = "LimitDescription = 'MML Landgroup'"
dissolvefields = ["OwnershipReferenceNumber", "Parish_In_CCB_BNG_NAME"]
dissolvefieldsFinal = ["OwnershipReferenceNumber", "Parish_In_CCB_BNG_NAME"]
dissolvefieldsTemp = ["OwnershipReferenceNumber"]
dissolveFieldsStats = 'SHAPE_Area MAX'
Output_Excel_File = r'C:\Users\UKPXR011\Desktop\StatsdissolvefieldsFinal\Montly_Parish_Stats\Ownership_Parish.xls'

#CSet the workspace
desktopPath = r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats'
working = r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Parish_Stats.gdb'

#set the environment
#SDE_Geodatabase = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde"

#arcpy.env.workspace = SDE_Geodatabase

print "Copying from SDE"
#Copy Layers from SDE
#Ownership =arcpy.Select_analysis(fc,str(working+"\Ownership"))
#Ownership = fc
#print "Ownership Copied"
#Ownership = r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Parish_Stats.gdb\Ownership'
#L3 = arcpy.Select_analysis(fc1,str(working+"\L3"),L3Query)
#print "L3 Copied"
#L3 = r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Parish_Stats.gdb\L3'
#MML = arcpy.Select_analysis(fc1,str(working+"\MML"),MMLQuery)
#print "MML Copied"
#MML = r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Parish_Stats.gdb\MML'
#CP3 =arcpy.Select_analysis(fc1,str(working+"\CP3"),CP3Query)
#print "CP3 Copied"
#CP3 = r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Parish_Stats.gdb\CP3'
#Parish = arcpy.Select_analysis(fc2,str(working+"\Parish"))
#print "Parish Copied"
#Parish = r'C:\Users\UKPXR011\Desktop\Stats\Montly_Parish_Stats\Parish_Stats.gdb\Parish'
#print "Made Local Copies"

#Merge L3 and MML
#L3_MML = arcpy.Merge_management([L3, MML],str(working)+"\L3_MML")
#print "L3 + MML Merged"

#Intersect Layers
#Intersect_Temp_L3 = arcpy.Intersect_analysis([Ownership,L3_MML], str(working)+"\LOwnership_L3", "ALL", "", "INPUT")
#Intersect_Temp_CP3 = arcpy.Intersect_analysis([Intersect_Temp_L3,CP3], str(working)+"\LOwnership_CP3", "ALL", "", "INPUT")
#Intersect_Temp_CP3_Parish = arcpy.Intersect_analysis([Intersect_Temp_CP3,Parish], str(working)+"\LOwnership_CP3_Parish", "ALL", "", "INPUT")
#print "Intersects Competed"

#Dissolve on Ownership Reference Number
#fc3= arcpy.Dissolve_management(Intersect_Temp_CP3_Parish,str(working)+"\Dissolve_CP3_Temp",dissolvefields)
fc3 = str(working)+"\Dissolve_CP3_Temp"
#fc4= arcpy.Dissolve_management(fc3,str(working)+"\Dissolve_Area_Max",dissolvefieldsTemp,dissolveFieldsStats)
fc4 = str(working)+"\Dissolve_Area_Max"
print "Dissolve Completed"

#Add a field called Parish

arcpy.AddField_management(fc3,"Max_Area",'DOUBLE')

print "Starting Search Cursor Madness"

# Use list comprehension to build a dictionary from a da SearchCursor
CursorJoinFields = ["OwnershipReferenceNumber",'MAX_SHAPE_Area']
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc4,CursorJoinFields)}

#print valueDict
#Delete the rows where the shape area doesnt match the max area (are not the largest duplicate)
with arcpy.da.UpdateCursor(fc3, ["OwnershipReferenceNumber",'Max_Area']) as updateRows:

    for updateRow in updateRows:
        keyValue = updateRow[0]
        if keyValue in valueDict:
            print 'made it'
            updateRow[1] = valueDict[keyValue][0]



del updateRows

print "cursor done"

#final intersect to get parish name against ownership reference numbers
#Intersect_Final_Temp = arcpy.Intersect_analysis([fc3,Parish], str(working)+"\Ownership_Parish_Temp", "ALL", "", "INPUT")
#Dissolve_Final = arcpy.Dissolve_management(Intersect_Final_Temp,str(working)+"\Dissolve_Ownership_Parish",dissolvefieldsFinal)
#arcpy.TableToExcel_conversion(Dissolve_Final, Output_Excel_File)
print "Finsihed"





