# File name: Safeguarding.py
# Author: Ollie Brown
# Date created: 20190904
# Date last modified: N/A
# Python Version: 2.7.13

# NOTE: The search and update cursors to clculate Local Authority and Constituency fields are outdated and need extra work, although they are producing the correct outcome.

# Import system modules
import arcpy
from datetime import *

#Capture start time of script
start = datetime.now()
print 'Safeguarding Started: %s\n' % (start)

# Set global variables
arcpy.env.overwriteOutput = True

# Change the workspace to where you would like the Project folder to be saved
workspace = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\Hop_Refresh"

# Change the name of the folder to the Project name
projectname = "HS2A_Safeguarding_20200127_HOP_Amendments"

# Create a container folder within the specified workspace containing the folder specified as Project Name above and dated to current date time
createprojectfolder = arcpy.CreateFolder_management(workspace, projectname+"_"+str(datetime.today().strftime('%Y%m%d_%H%M%S')))

# Create required FGDBs for Output, WebGIS storage and Working data
Output = arcpy.CreateFileGDB_management(createprojectfolder,"Output.gdb")
Working = arcpy.CreateFileGDB_management(createprojectfolder,"Working.gdb")

# Set local variables
LOPField = "OwnershipReferenceNumber"
FieldType = "DOUBLE"
intfieldtype = "SHORT"

# Analytical fields to be added
newsurfaceareafield = "SGSurArea_NEW"
oldsurfaceareafield = "SGSurArea_OLD"
newsubsurfaceareafield = "SGSubArea_NEW"
oldsubsurfaceareafield = "SGSubArea_OLD"
newEHPZ1areafield = "EHPZ1Area_NEW"
oldEHPZ1areafield = "EHPZ1Area_OLD"
newEHPZ2areafield = "EHPZ2Area_NEW"
oldEHPZ2areafield = "EHPZ2Area_OLD"
newRSZareafield = "RSZArea_NEW"
oldRSZareafield = "RSZArea_OLD"
newHOP1areafield = "HOP1Area_NEW"
oldHOP1areafield = "HOP1Area_OLD"
newHOP2areafield = "HOP2Area_NEW"
oldHOP2areafield = "HOP2Area_OLD"
newHOP3areafield = "HOP3Area_NEW"
oldHOP3areafield = "HOP3Area_OLD"
newsurfacepercentagefield = "SGSurPercentage_NEW"
oldsurfacepercentagefield = "SGSurPercentage_OLD"
newsubsurfacepercentagefield = "SGSubPercentage_NEW"
oldsubsurfacepercentagefield = "SGSubPercentage_OLD"
newEHPZ1percentagefield = "EHPZ1Percentage_NEW"
oldEHPZ1percentagefield = "EHPZ1Percentage_OLD"
newEHPZ2percentagefield = "EHPZ2Percentage_NEW"
oldEHPZ2percentagefield = "EHPZ2Percentage_OLD"
newRSZpercentagefield = "RSZPercentage_NEW"
oldRSZpercentagefield = "RSZPercentage_OLD"
newHOP1percentagefield = "HOP1Percentage_NEW"
oldHOP1percentagefield = "HOP1Percentage_OLD"
newHOP2percentagefield = "HOP2Percentage_NEW"
oldHOP2percentagefield = "HOP2Percentage_OLD"
newHOP3percentagefield = "HOP3Percentage_NEW"
oldHOP3percentagefield = "HOP3Percentage_OLD"
newSGSurIntegerfield = "SGSurInteger_NEW"
oldSGSurIntegerfield = "SGSurInteger_OLD"
newSGSubIntegerfield = "SGSubInteger_NEW"
oldSGSubIntegerfield = "SGSubInteger_OLD"
newEHPZ1Integerfield = "EHPZ1Integer_NEW"
oldEHPZ1Integerfield = "EHPZ1Integer_OLD"
newEHPZ2Integerfield = "EHPZ2Integer_NEW"
oldEHPZ2Integerfield = "EHPZ2Integer_OLD"
newRSZIntegerfield = "RSZInteger_NEW"
oldRSZIntegerfield = "RSZInteger_OLD"
newHOP1Integerfield = "HOP1Integer_NEW"
oldHOP1Integerfield = "HOP1Integer_OLD"
newHOP2Integerfield = "HOP2Integer_NEW"
oldHOP2Integerfield = "HOP2Integer_OLD"
newHOP3Integerfield = "HOP3Integer_NEW"
oldHOP3Integerfield = "HOP3Integer_OLD"
newHOPTotalareafield = "HOPTotalArea"
newHOPTotalpercentagefield = "HOPTotalPercentage"
InHOPfield = "In_HOP"
NewNoZonefield = "No_Zone_NEW"
OldNoZonefield = "No_Zone_OLD"
AddressPresentField = "Contains_Address"
scenario = "Scenario"
scenariotext = "Scenario_Text"
gisreview = "GIS_Review"
exclusion = "Exclusion_Reason"
HOPScenario = "HOP_Scenario"
HOPScenariotext = "HOP_Scenario_Text"

# List Input Feature Classes
HMLRTitles = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\Hop_Refresh\HOP_Update_16122020.gdb\STATUTORY_PROCESSES\HMLR_Parcels"
LandOwnershipParcels = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\Hop_Refresh\HOP_Update_16122020.gdb\SLOPS"
NewSafeguardingZones = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\C863-MCL-GI-GDD-000-000005_P11\C863-MCL-GI-GDD-000-000005_P11\C863-MCL-GI-GDD-000-000005_P11\Y20W12.gdb\HS2_HSTWO_SafeguardingAndZonedPropertySchemes_Ply"
OldSafeguardingZones = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\Data\Data.gdb\HS2_HSTWO_SafeguardingAndZonedPropertySchemes_Ply"
LocalAuthority = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\Local_Authority_Districts_December_2017_Full_Clipped_Boundaries_in_Great_Britain\Local_Authority_Districts_December_2017_Full_Clipped_Boundaries_in_Great_Britain.shp"
Constituency = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\Westminster_Parliamentary_Constituencies_December_2015\Westminster_Parliamentary_Constituencies_December_2015_Generalised_Clipped_Boundaries_in_Great_Britain.shp"
AddressPoly = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\Relates_Update\ABP_Relates.gdb\STATUTORY_PROCESSES\ABP_Polygon"
AddressNonPoly = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\Relates_Update\ABP_Relates.gdb\STATUTORY_PROCESSES\ABP_NonPolygon"

# Take a copy of Land Ownerships and move to the working folder so that the input data is not changed in anyway
CopyLOP = arcpy.Select_analysis(LandOwnershipParcels, str(Working)+"\Parcel_LOP")

print "Create working copy of Land Ownership Parcel complete"

# Select the required zones from the input Safeguarding data
SelectNewZones = arcpy.Select_analysis(NewSafeguardingZones, str(Working)+"\Parcel_ZoneSelectNew", """Zone_Type <> 'SGLim' AND Currency = 'Current' AND HS2_Phase = 'R3'""")
SelectOldZones = arcpy.Select_analysis(OldSafeguardingZones, str(Working)+"\Parcel_ZoneSelectOld", """Zone_Type <> 'SGLim' AND Currency = 'Current' AND HS2_Phase = 'R3'""")

print "Required safeguarding zone selection complete"

# Intersect the Land Ownership Parcels with the Safeguarding Zones
IntersectNewZones = arcpy.Intersect_analysis([CopyLOP,SelectNewZones], str(Working)+"\Parcel_ZoneIntersectNew", "ALL", "", "INPUT")
IntersectOldZones = arcpy.Intersect_analysis([CopyLOP,SelectOldZones], str(Working)+"\Parcel_ZoneIntersectOld", "ALL", "", "INPUT")

print "Required safeguarding zone intersection with working Land Ownership Parcel complete"

# Dissolve the intersected LOP and Safeguarding Zones
DissolveNewZones = arcpy.Dissolve_management(IntersectNewZones, str(Working)+"\Parcel_ZoneDissolveNew", [LOPField,"Zone_Type"], "", "", "")
DissolveOldZones = arcpy.Dissolve_management(IntersectOldZones, str(Working)+"\Parcel_ZoneDissolveOld", [LOPField,"Zone_Type"], "", "", "")

print "Ownershipreferencenumber and safeguarding zone dissolve complete"

# Search for OwnershipReferenceNumber in CopyLOP and add to set
CopyLOPset = set(r[0] for r in arcpy.da.SearchCursor (CopyLOP,LOPField))
DissolveNewZonesset = set(r[0] for r in arcpy.da.SearchCursor (DissolveNewZones,LOPField))
DissolveOldZonesset = set(r[0] for r in arcpy.da.SearchCursor (DissolveOldZones,LOPField))

# Union sets created from search cursors which look for unique OwnershipReferenceNumbers between the dissolves of the intersected LOP and Safeguarding Zones above
UnionSet = DissolveNewZonesset|DissolveOldZonesset

# Generate a set of Land Ownership Parcels that intersect with the new and old Safeguarding zones by generating a set of OwnershipReferenceNumbers that keeps only those references that exist within the union set above
ToincludeinSafeguardingAnalysis = CopyLOPset & UnionSet

# Convert the set of OwnershipReferenceNumbers to a string for use in the where clause
LOPliststring = ",".join("%s" % r for r in ToincludeinSafeguardingAnalysis)

# Create a where clause for use in select below
where_clause = ("""OwnershipReferenceNumber in(%s)""" % LOPliststring)

# Select only LOP that intersects with new or old Safeguarding boundaries
requiredLOP = arcpy.Select_analysis(CopyLOP, str(Output)+"\Required_LOP", where_clause)
print "Select participating Land Ownership Parcel complete"

# Calculate and join total area of LOP to dissolved layers for use in further calculations
addtotalLOParea = arcpy.AddField_management(requiredLOP, "Total_LOP_Area", FieldType, "",field_alias="Total LOP Area")
calculatetotalLOParea = arcpy.CalculateField_management(addtotalLOParea, "Total_LOP_Area", """!Shape_Area!""", "PYTHON_9.3")
joinnewtotalLOParea = arcpy.JoinField_management(DissolveNewZones, LOPField, calculatetotalLOParea, LOPField, "Total_LOP_Area")
joinoldtotalLOParea = arcpy.JoinField_management(DissolveOldZones, LOPField, calculatetotalLOParea, LOPField, "Total_LOP_Area")

print "Join total LOP area field complete"

# Add Intersection, percentage and integer fields to dissolved layers
addsurfaceareanew = arcpy.AddField_management(joinnewtotalLOParea, newsurfaceareafield, FieldType, "",field_alias="Surface Area New")
addsurfacepercentagenew = arcpy.AddField_management(joinnewtotalLOParea, newsurfacepercentagefield, FieldType, "",field_alias="Surface Percentage New")
addSGSurIntegernew = arcpy.AddField_management(joinnewtotalLOParea, newSGSurIntegerfield, intfieldtype, "",field_alias="Surface Integer New")

addsurfaceareaold = arcpy.AddField_management(joinoldtotalLOParea, oldsurfaceareafield, FieldType, "",field_alias="Surface Area Old")
addsurfacepercentageold = arcpy.AddField_management(joinoldtotalLOParea, oldsurfacepercentagefield, FieldType, "",field_alias="Surface Percentage Old")
addSGSurIntegerold = arcpy.AddField_management(joinoldtotalLOParea, oldSGSurIntegerfield, intfieldtype, "",field_alias="Surface Integer Old")

addsubsurfaceareanew = arcpy.AddField_management(joinnewtotalLOParea, newsubsurfaceareafield, FieldType, "",field_alias="SubSurface Area New")
addsubsurfacepercentagenew = arcpy.AddField_management(joinnewtotalLOParea, newsubsurfacepercentagefield, FieldType, "",field_alias="SubSurface Percentage New")
addSGSubIntegernew = arcpy.AddField_management(joinnewtotalLOParea, newSGSubIntegerfield , intfieldtype, "",field_alias="SubSurface Integer New")

addsubsurfaceareaold = arcpy.AddField_management(joinoldtotalLOParea, oldsubsurfaceareafield, FieldType, "",field_alias="SubSurface Area Old")
addsubsurfacepercentageold = arcpy.AddField_management(joinoldtotalLOParea, oldsubsurfacepercentagefield, FieldType, "",field_alias="SubSurface Percentage Old")
addSGSubIntegerold = arcpy.AddField_management(joinoldtotalLOParea, oldSGSubIntegerfield, intfieldtype, "",field_alias="SubSurface Integer Old")

addEHPZ1areanew = arcpy.AddField_management(joinnewtotalLOParea, newEHPZ1areafield, FieldType, "",field_alias="EHPZ1 Area New")
addEHPZ1percentagenew = arcpy.AddField_management(joinnewtotalLOParea, newEHPZ1percentagefield, FieldType, "",field_alias="EHPZ1 Percentage New")
addEHPZ1Integernew = arcpy.AddField_management(joinnewtotalLOParea, newEHPZ1Integerfield, intfieldtype, "",field_alias="EHPZ1 Integer New")

addEHPZ1areaold = arcpy.AddField_management(joinoldtotalLOParea, oldEHPZ1areafield, FieldType, "",field_alias="EHPZ1 Area Old")
addEHPZ1percentageold = arcpy.AddField_management(joinoldtotalLOParea, oldEHPZ1percentagefield, FieldType, "",field_alias="EHPZ1 Percentage Old")
addEHPZ1Integerold = arcpy.AddField_management(joinoldtotalLOParea, oldEHPZ1Integerfield, intfieldtype, "",field_alias="EHPZ1 Integer Old")

addEHPZ2areanew = arcpy.AddField_management(joinnewtotalLOParea, newEHPZ2areafield, FieldType, "",field_alias="EHPZ2 Area New")
addEHPZ2percentagenew = arcpy.AddField_management(joinnewtotalLOParea, newEHPZ2percentagefield, FieldType, "",field_alias="EHPZ2 Percentage New")
addEHPZ2Integernew = arcpy.AddField_management(joinnewtotalLOParea, newEHPZ2Integerfield, intfieldtype, "",field_alias="EHPZ2 Integer New")

addEHPZ2areaold = arcpy.AddField_management(joinoldtotalLOParea, oldEHPZ2areafield, FieldType, "",field_alias="EHPZ2 Area Old")
addEHPZ2percentageold = arcpy.AddField_management(joinoldtotalLOParea, oldEHPZ2percentagefield, FieldType, "",field_alias="EHPZ2 Percentage Old")
addEHPZ2Integerold = arcpy.AddField_management(joinoldtotalLOParea, oldEHPZ2Integerfield, intfieldtype, "",field_alias="EHPZ2 Integer Old")

addRSZareanew = arcpy.AddField_management(joinnewtotalLOParea, newRSZareafield, FieldType, "",field_alias="RSZ Area New")
addRSZpercentagenew = arcpy.AddField_management(joinnewtotalLOParea, newRSZpercentagefield, FieldType, "",field_alias="RSZ Percentage New")
addRSZIntegernew = arcpy.AddField_management(joinnewtotalLOParea, newRSZIntegerfield, intfieldtype, "",field_alias="RSZ Integer New")

addRSZareaold = arcpy.AddField_management(joinoldtotalLOParea, oldRSZareafield, FieldType, "",field_alias="RSZ Area Old")
addRSZpercentageold = arcpy.AddField_management(joinoldtotalLOParea, oldRSZpercentagefield, FieldType, "",field_alias="RSZ Percentage Old")
addRSZIntegerold = arcpy.AddField_management(joinoldtotalLOParea, oldRSZIntegerfield, intfieldtype, "",field_alias="RSZ Integer Old")

addHOP1areanew = arcpy.AddField_management(joinnewtotalLOParea, newHOP1areafield, FieldType, "",field_alias="HOP1 Area New")
addHOP1percentagenew = arcpy.AddField_management(joinnewtotalLOParea, newHOP1percentagefield, FieldType, "",field_alias="HOP1 Percentage New")
addHOP1Integernew = arcpy.AddField_management(joinnewtotalLOParea, newHOP1Integerfield, intfieldtype, "",field_alias="HOP1 Integer New")

addHOP1areaold = arcpy.AddField_management(joinoldtotalLOParea, oldHOP1areafield, FieldType, "",field_alias="HOP1 Area Old")
addHOP1percentageold = arcpy.AddField_management(joinoldtotalLOParea, oldHOP1percentagefield, FieldType, "",field_alias="HOP1 Percentage Old")
addHOP1Integerold = arcpy.AddField_management(joinoldtotalLOParea, oldHOP1Integerfield, intfieldtype, "",field_alias="HOP1 Integer Old")

addHOP2areanew = arcpy.AddField_management(joinnewtotalLOParea, newHOP2areafield, FieldType, "",field_alias="HOP2 Area New")
addHOP2percentagenew = arcpy.AddField_management(joinnewtotalLOParea, newHOP2percentagefield, FieldType, "",field_alias="HOP2 Percentage New")
addHOP2Integernew = arcpy.AddField_management(joinnewtotalLOParea, newHOP2Integerfield, intfieldtype, "",field_alias="HOP2 Integer New")

addHOP2areaold = arcpy.AddField_management(joinoldtotalLOParea, oldHOP2areafield, FieldType, "",field_alias="HOP2 Area Old")
addHOP2percentageold = arcpy.AddField_management(joinoldtotalLOParea, oldHOP2percentagefield, FieldType, "",field_alias="HOP2 Percentage Old")
addHOP2Integerold = arcpy.AddField_management(joinoldtotalLOParea, oldHOP2Integerfield, intfieldtype, "",field_alias="HOP2 Integer Old")

addHOP3areanew = arcpy.AddField_management(joinnewtotalLOParea, newHOP3areafield, FieldType, "",field_alias="HOP3 Area New")
addHOP3percentagenew = arcpy.AddField_management(joinnewtotalLOParea, newHOP3percentagefield, FieldType, "",field_alias="HOP3 Percentage New")
addHOP3Integernew = arcpy.AddField_management(joinnewtotalLOParea, newHOP3Integerfield, intfieldtype, "",field_alias="HOP3 Integer New")

addHOP3areaold = arcpy.AddField_management(joinoldtotalLOParea, oldHOP3areafield, FieldType, "",field_alias="HOP3 Area Old")
addHOP3percentageold = arcpy.AddField_management(joinoldtotalLOParea, oldHOP3percentagefield, FieldType, "",field_alias="HOP3 Percentage Old")
addHOP3Integerold = arcpy.AddField_management(joinoldtotalLOParea, oldHOP3Integerfield, intfieldtype, "",field_alias="HOP3 Integer Old")

print "Intersection, percentage and integer field addition complete"

areafieldlistnew = ["ZONE_TYPE","SHAPE_AREA",newsurfaceareafield,newsubsurfaceareafield,newEHPZ1areafield,newEHPZ2areafield,newRSZareafield,newHOP1areafield,newHOP2areafield,newHOP3areafield]
areafieldlistold = ["ZONE_TYPE","SHAPE_AREA",oldsurfaceareafield,oldsubsurfaceareafield,oldEHPZ1areafield,oldEHPZ2areafield,oldRSZareafield,oldHOP1areafield,oldHOP2areafield,oldHOP3areafield]

# Update new intersection areas within feature class with SHAPE_AREA values
with arcpy.da.UpdateCursor(joinnewtotalLOParea, areafieldlistnew) as cursor:
    # For each field, evaluate the value within it. If the value is Null then update to 0
    for rownewarea in cursor:
        if rownewarea[0] == 'SGSur':
            rownewarea[2] = rownewarea[1]
        elif rownewarea[0] == 'SGSub':
            rownewarea[3] = rownewarea[1]
        elif rownewarea[0] == 'EHPZ1':
            rownewarea[4] = rownewarea[1]
        elif rownewarea[0] == 'EHPZ2':
            rownewarea[5] = rownewarea[1]
        elif rownewarea[0] == 'RSZ':
            rownewarea[6] = rownewarea[1]
        elif rownewarea[0] == 'HOP1':
            rownewarea[7] = rownewarea[1]
        elif rownewarea[0] == 'HOP2':
            rownewarea[8] = rownewarea[1]
        elif rownewarea[0] == 'HOP3':
            rownewarea[9] = rownewarea[1]
        # Update the cursor with the updated list
        cursor.updateRow(rownewarea)

# Update old intersection areas within feature class with SHAPE_AREA values
with arcpy.da.UpdateCursor(joinoldtotalLOParea, areafieldlistold) as cursor:
    # For each field, evaluate the value within it. If the value is Null then update to 0
    for rowoldarea in cursor:
        if rowoldarea[0] == 'SGSur':
            rowoldarea[2] = rowoldarea[1]
        elif rowoldarea[0] == 'SGSub':
            rowoldarea[3] = rowoldarea[1]
        elif rowoldarea[0] == 'EHPZ1':
            rowoldarea[4] = rowoldarea[1]
        elif rowoldarea[0] == 'EHPZ2':
            rowoldarea[5] = rowoldarea[1]
        elif rowoldarea[0] == 'RSZ':
            rowoldarea[6] = rowoldarea[1]
        elif rowoldarea[0] == 'HOP1':
            rowoldarea[7] = rowoldarea[1]
        elif rowoldarea[0] == 'HOP2':
            rowoldarea[8] = rowoldarea[1]
        elif rowoldarea[0] == 'HOP3':
            rowoldarea[9] = rowoldarea[1]
        # Update the cursor with the updated list
        cursor.updateRow(rowoldarea)

print "Intersection area calculation complete"

# Calculate percentage fields
calculatesurfacepercentagenew = arcpy.CalculateField_management(addsurfacepercentagenew, newsurfacepercentagefield, """100 if !SGSurArea_NEW!/ !Total_LOP_Area!*100 > 100 else !SGSurArea_NEW!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculatesurfacepercentageold = arcpy.CalculateField_management(addsurfacepercentageold, oldsurfacepercentagefield, """100 if !SGSurArea_OLD!/ !Total_LOP_Area!*100 > 100 else !SGSurArea_OLD!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculatesubsurfacepercentagenew = arcpy.CalculateField_management(addsubsurfacepercentagenew, newsubsurfacepercentagefield, """100 if !SGSubArea_NEW!/ !Total_LOP_Area!*100 > 100 else !SGSubArea_NEW!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculatesubsurfacepercentageold = arcpy.CalculateField_management(addsubsurfacepercentageold, oldsubsurfacepercentagefield, """100 if !SGSubArea_OLD!/ !Total_LOP_Area!*100 > 100 else !SGSubArea_OLD!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateEHPZ1percentagenew = arcpy.CalculateField_management(addEHPZ1percentagenew, newEHPZ1percentagefield, """100 if !EHPZ1Area_NEW!/ !Total_LOP_Area!*100 > 100 else !EHPZ1Area_NEW!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateEHPZ1percentageold = arcpy.CalculateField_management(addEHPZ1percentageold, oldEHPZ1percentagefield, """100 if !EHPZ1Area_OLD!/ !Total_LOP_Area!*100 > 100 else !EHPZ1Area_OLD!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateEHPZ2percentagenew = arcpy.CalculateField_management(addEHPZ2percentagenew, newEHPZ2percentagefield, """100 if !EHPZ2Area_NEW!/ !Total_LOP_Area!*100 > 100 else !EHPZ2Area_NEW!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateEHPZ2percentageold = arcpy.CalculateField_management(addEHPZ2percentageold, oldEHPZ2percentagefield, """100 if !EHPZ2Area_OLD!/ !Total_LOP_Area!*100 > 100 else !EHPZ2Area_OLD!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateRSZpercentagenew = arcpy.CalculateField_management(addRSZpercentagenew, newRSZpercentagefield, """100 if !RSZArea_NEW!/ !Total_LOP_Area!*100 > 100 else !RSZArea_NEW!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateRSZpercentageold = arcpy.CalculateField_management(addRSZpercentageold, oldRSZpercentagefield, """100 if !RSZArea_OLD!/ !Total_LOP_Area!*100 > 100 else !RSZArea_OLD!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateHOP1percentagenew = arcpy.CalculateField_management(addHOP1percentagenew, newHOP1percentagefield, """100 if !HOP1Area_NEW!/ !Total_LOP_Area!*100 > 100 else !HOP1Area_NEW!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateHOP1percentageold = arcpy.CalculateField_management(addHOP1percentageold, oldHOP1percentagefield, """100 if !HOP1Area_OLD!/ !Total_LOP_Area!*100 > 100 else !HOP1Area_OLD!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateHOP2percentagenew = arcpy.CalculateField_management(addHOP2percentagenew, newHOP2percentagefield, """100 if !HOP2Area_NEW!/ !Total_LOP_Area!*100 > 100 else !HOP2Area_NEW!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateHOP2percentageold = arcpy.CalculateField_management(addHOP2percentageold, oldHOP2percentagefield, """100 if !HOP2Area_OLD!/ !Total_LOP_Area!*100 > 100 else !HOP2Area_OLD!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateHOP3percentagenew = arcpy.CalculateField_management(addHOP3percentagenew, newHOP3percentagefield, """100 if !HOP3Area_NEW!/ !Total_LOP_Area!*100 > 100 else !HOP3Area_NEW!/ !Total_LOP_Area!*100""", "PYTHON_9.3")
calculateHOP3percentageold = arcpy.CalculateField_management(addHOP3percentageold, oldHOP3percentagefield, """100 if !HOP3Area_OLD!/ !Total_LOP_Area!*100 > 100 else !HOP3Area_OLD!/ !Total_LOP_Area!*100""", "PYTHON_9.3")

print "Intersection percentage calculation complete"

# Calculate integer fields
calculatesurfaceintnew = arcpy.CalculateField_management(calculateHOP3percentagenew, newSGSurIntegerfield, """1 if !SGSurArea_NEW! >=1 else None""", "PYTHON_9.3")
calculatesurfaceintold = arcpy.CalculateField_management(calculateHOP3percentageold, oldSGSurIntegerfield, """1 if !SGSurArea_OLD! >=1 else None""", "PYTHON_9.3")
calculatesubsurfaceintnew = arcpy.CalculateField_management(calculateHOP3percentagenew, newSGSubIntegerfield, """1 if !SGSubArea_NEW! >=1 else None""", "PYTHON_9.3")
calculatesubsurfaceintold = arcpy.CalculateField_management(calculateHOP3percentageold, oldSGSubIntegerfield, """1 if !SGSubArea_OLD! >=1 else None""", "PYTHON_9.3")
calculateEHPZ1surfaceintnew = arcpy.CalculateField_management(calculateHOP3percentagenew, newEHPZ1Integerfield, """1 if !EHPZ1Area_NEW! >=1 else None""", "PYTHON_9.3")
calculateEHPZ1surfaceintold = arcpy.CalculateField_management(calculateHOP3percentageold, oldEHPZ1Integerfield, """1 if !EHPZ1Area_OLD! >=1 else None""", "PYTHON_9.3")
calculateEHPZ2surfaceintnew = arcpy.CalculateField_management(calculateHOP3percentagenew, newEHPZ2Integerfield, """1 if !EHPZ2Area_NEW! >=1 else None""", "PYTHON_9.3")
calculateEHPZ2surfaceintold = arcpy.CalculateField_management(calculateHOP3percentageold, oldEHPZ2Integerfield, """1 if !EHPZ2Area_OLD! >=1 else None""", "PYTHON_9.3")
calculateRSZsurfaceintnew = arcpy.CalculateField_management(calculateHOP3percentagenew, newRSZIntegerfield, """1 if !RSZArea_NEW! >=1 else None""", "PYTHON_9.3")
calculateRSZsurfaceintold = arcpy.CalculateField_management(calculateHOP3percentageold, oldRSZIntegerfield, """1 if !RSZArea_OLD! >=1 else None""", "PYTHON_9.3")
calculateHOP1surfaceintnew = arcpy.CalculateField_management(calculateHOP3percentagenew, newHOP1Integerfield, """1 if !HOP1Area_NEW! >=1 else None""", "PYTHON_9.3")
calculateHOP1surfaceintold = arcpy.CalculateField_management(calculateHOP3percentageold, oldHOP1Integerfield, """1 if !HOP1Area_OLD! >=1 else None""", "PYTHON_9.3")
calculateHOP2surfaceintnew = arcpy.CalculateField_management(calculateHOP3percentagenew, newHOP2Integerfield, """1 if !HOP2Area_NEW! >=1 else None""", "PYTHON_9.3")
calculateHOP2surfaceintold = arcpy.CalculateField_management(calculateHOP3percentageold, oldHOP2Integerfield, """1 if !HOP2Area_OLD! >=1 else None""", "PYTHON_9.3")
calculateHOP3surfaceintnew = arcpy.CalculateField_management(calculateHOP3percentagenew, newHOP3Integerfield, """1 if !HOP3Area_NEW! >=1 else None""", "PYTHON_9.3")
calculateHOP3surfaceintold = arcpy.CalculateField_management(calculateHOP3percentageold, oldHOP3Integerfield, """1 if !HOP3Area_OLD! >=1 else None""", "PYTHON_9.3")

print "Intersection integer calculation complete"

# Select zone for join

newsurfaceselect = arcpy.Select_analysis(calculateHOP3surfaceintnew, str(Working)+"\Parcel_SGSurnew", """Zone_Type = 'SGSur'""")
oldsurfaceselect = arcpy.Select_analysis(calculateHOP3surfaceintold, str(Working)+"\Parcel_SGSurold", """Zone_Type = 'SGSur'""")
newsubselect = arcpy.Select_analysis(calculateHOP3surfaceintnew, str(Working)+"\Parcel_SGSubnew", """Zone_Type = 'SGSub'""")
oldsubselect = arcpy.Select_analysis(calculateHOP3surfaceintold, str(Working)+"\Parcel_SGSubold", """Zone_Type = 'SGSub'""")
newEHPZ1select = arcpy.Select_analysis(calculateHOP3surfaceintnew, str(Working)+"\Parcel_EHPZ1new", """Zone_Type = 'EHPZ1'""")
oldEHPZ1select = arcpy.Select_analysis(calculateHOP3surfaceintold, str(Working)+"\Parcel_EHPZ1old", """Zone_Type = 'EHPZ1'""")
newEHPZ2select = arcpy.Select_analysis(calculateHOP3surfaceintnew, str(Working)+"\Parcel_EHPZ2new", """Zone_Type = 'EHPZ2'""")
oldEHPZ2select = arcpy.Select_analysis(calculateHOP3surfaceintold, str(Working)+"\Parcel_EHPZ2old", """Zone_Type = 'EHPZ2'""")
newRSZselect = arcpy.Select_analysis(calculateHOP3surfaceintnew, str(Working)+"\Parcel_RSZnew", """Zone_Type = 'RSZ'""")
oldRSZselect = arcpy.Select_analysis(calculateHOP3surfaceintold, str(Working)+"\Parcel_RSZold", """Zone_Type = 'RSZ'""")
newHOP1select = arcpy.Select_analysis(calculateHOP3surfaceintnew, str(Working)+"\Parcel_HOP1new", """Zone_Type = 'HOP1'""")
oldHOP1select = arcpy.Select_analysis(calculateHOP3surfaceintold, str(Working)+"\Parcel_HOP1old", """Zone_Type = 'HOP1'""")
newHOP2select = arcpy.Select_analysis(calculateHOP3surfaceintnew, str(Working)+"\Parcel_HOP2new", """Zone_Type = 'HOP2'""")
oldHOP2select = arcpy.Select_analysis(calculateHOP3surfaceintold, str(Working)+"\Parcel_HOP2old", """Zone_Type = 'HOP2'""")
newHOP3select = arcpy.Select_analysis(calculateHOP3surfaceintnew, str(Working)+"\Parcel_HOP3new", """Zone_Type = 'HOP3'""")
oldHOP3select = arcpy.Select_analysis(calculateHOP3surfaceintold, str(Working)+"\Parcel_HOP3old", """Zone_Type = 'HOP3'""")

print "Zone selection for join complete"

# Join fields back to final output
joinnewsurfacefields = arcpy.JoinField_management(requiredLOP, LOPField, newsurfaceselect, LOPField, ["SGSurArea_NEW","SGSurPercentage_NEW","SGSurInteger_NEW"])
joinoldsurfacefields = arcpy.JoinField_management(joinnewsurfacefields, LOPField, oldsurfaceselect, LOPField, ["SGSurArea_OLD","SGSurPercentage_OLD","SGSurInteger_OLD"])
joinnewsubsurfacefields = arcpy.JoinField_management(joinoldsurfacefields, LOPField, newsubselect, LOPField, ["SGSubArea_NEW","SGSubPercentage_NEW","SGSubInteger_NEW"])
joinoldsubsurfacefields = arcpy.JoinField_management(joinnewsubsurfacefields, LOPField, oldsubselect, LOPField, ["SGSubArea_OLD","SGSubPercentage_OLD","SGSubInteger_OLD"])
joinnewEHPZ1fields = arcpy.JoinField_management(joinoldsubsurfacefields, LOPField, newEHPZ1select, LOPField, ["EHPZ1Area_NEW","EHPZ1Percentage_NEW","EHPZ1Integer_NEW"])
joinoldEHPZ1fields = arcpy.JoinField_management(joinnewEHPZ1fields, LOPField, oldEHPZ1select, LOPField, ["EHPZ1Area_OLD","EHPZ1Percentage_OLD","EHPZ1Integer_OLD"])
joinnewEHPZ2fields = arcpy.JoinField_management(joinoldEHPZ1fields, LOPField, newEHPZ2select, LOPField, ["EHPZ2Area_NEW","EHPZ2Percentage_NEW","EHPZ2Integer_NEW"])
joinoldEHPZ2fields = arcpy.JoinField_management(joinnewEHPZ2fields, LOPField, oldEHPZ2select, LOPField, ["EHPZ2Area_OLD","EHPZ2Percentage_OLD","EHPZ2Integer_OLD"])
joinnewRSZfields = arcpy.JoinField_management(joinoldEHPZ2fields, LOPField, newRSZselect, LOPField, ["RSZArea_NEW","RSZPercentage_NEW","RSZInteger_NEW"])
joinoldRSZfields = arcpy.JoinField_management(joinnewRSZfields, LOPField, oldRSZselect, LOPField, ["RSZArea_OLD","RSZPercentage_OLD","RSZInteger_OLD"])
joinnewHOP1fields = arcpy.JoinField_management(joinoldRSZfields, LOPField, newHOP1select, LOPField, ["HOP1Area_NEW","HOP1Percentage_NEW","HOP1Integer_NEW"])
joinoldHOP1fields = arcpy.JoinField_management(joinnewHOP1fields, LOPField, oldHOP1select, LOPField, ["HOP1Area_OLD","HOP1Percentage_OLD","HOP1Integer_OLD"])
joinnewHOP2fields = arcpy.JoinField_management(joinoldHOP1fields, LOPField, newHOP2select, LOPField, ["HOP2Area_NEW","HOP2Percentage_NEW","HOP2Integer_NEW"])
joinoldHOP2fields = arcpy.JoinField_management(joinnewHOP2fields, LOPField, oldHOP2select, LOPField, ["HOP2Area_OLD","HOP2Percentage_OLD","HOP2Integer_OLD"])
joinnewHOP3fields = arcpy.JoinField_management(joinoldHOP2fields, LOPField, newHOP3select, LOPField, ["HOP3Area_NEW","HOP3Percentage_NEW","HOP3Integer_NEW"])
joinoldHOP3fields = arcpy.JoinField_management(joinnewHOP3fields, LOPField, oldHOP3select, LOPField, ["HOP3Area_OLD","HOP3Percentage_OLD","HOP3Integer_OLD"])

print "Intersection, percentage and integer fields join to participating Land Ownership Parcels complete"

# Calculate zero values for areas
calculatesurfaceareanew = arcpy.CalculateField_management(joinoldHOP3fields, newsurfaceareafield, """!SGSurArea_NEW! if !SGSurArea_NEW! > 0 else 0""", "PYTHON_9.3")
calculatesurfaceareaold = arcpy.CalculateField_management(joinoldHOP3fields, oldsurfaceareafield, """!SGSurArea_OLD! if !SGSurArea_OLD! > 0 else 0""", "PYTHON_9.3")
calculatesubsurfaceareanew = arcpy.CalculateField_management(joinoldHOP3fields, newsubsurfaceareafield, """!SGSubArea_NEW! if !SGSubArea_NEW! > 0 else 0""", "PYTHON_9.3")
calculatesubsurfaceareaold = arcpy.CalculateField_management(joinoldHOP3fields, oldsubsurfaceareafield, """!SGSubArea_OLD! if !SGSubArea_OLD! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ1areanew = arcpy.CalculateField_management(joinoldHOP3fields, newEHPZ1areafield, """!EHPZ1Area_NEW! if !EHPZ1Area_NEW! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ1areaold = arcpy.CalculateField_management(joinoldHOP3fields, oldEHPZ1areafield, """!EHPZ1Area_OLD! if !EHPZ1Area_OLD! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ2areanew = arcpy.CalculateField_management(joinoldHOP3fields, newEHPZ2areafield, """!EHPZ2Area_NEW! if !EHPZ2Area_NEW! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ2areaold = arcpy.CalculateField_management(joinoldHOP3fields, oldEHPZ2areafield, """!EHPZ2Area_OLD! if !EHPZ2Area_OLD! > 0 else 0""", "PYTHON_9.3")
calculateRSZareanew = arcpy.CalculateField_management(joinoldHOP3fields, newRSZareafield, """!RSZArea_NEW! if !RSZArea_NEW! > 0 else 0""", "PYTHON_9.3")
calculateRSZareaold = arcpy.CalculateField_management(joinoldHOP3fields, oldRSZareafield, """!RSZArea_OLD! if !RSZArea_OLD! > 0 else 0""", "PYTHON_9.3")
calculateHOP1areanew = arcpy.CalculateField_management(joinoldHOP3fields, newHOP1areafield, """!HOP1Area_NEW! if !HOP1Area_NEW! > 0 else 0""", "PYTHON_9.3")
calculateHOP1areaold = arcpy.CalculateField_management(joinoldHOP3fields, oldHOP1areafield, """!HOP1Area_OLD! if !HOP1Area_OLD! > 0 else 0""", "PYTHON_9.3")
calculateHOP2areanew = arcpy.CalculateField_management(joinoldHOP3fields, newHOP2areafield, """!HOP2Area_NEW! if !HOP2Area_NEW! > 0 else 0""", "PYTHON_9.3")
calculateHOP2areaold = arcpy.CalculateField_management(joinoldHOP3fields, oldHOP2areafield, """!HOP2Area_OLD! if !HOP2Area_OLD! > 0 else 0""", "PYTHON_9.3")
calculateHOP3areanew = arcpy.CalculateField_management(joinoldHOP3fields, newHOP3areafield, """!HOP3Area_NEW! if !HOP3Area_NEW! > 0 else 0""", "PYTHON_9.3")
calculateHOP3areaold = arcpy.CalculateField_management(joinoldHOP3fields, oldHOP3areafield, """!HOP3Area_OLD! if !HOP3Area_OLD! > 0 else 0""", "PYTHON_9.3")
calculatesurfacepercentagenew = arcpy.CalculateField_management(joinoldHOP3fields, newsurfacepercentagefield, """!SGSurPercentage_NEW! if !SGSurPercentage_NEW! > 0 else 0""", "PYTHON_9.3")
calculatesurfacepercentageold = arcpy.CalculateField_management(joinoldHOP3fields, oldsurfacepercentagefield, """!SGSurPercentage_OLD! if !SGSurPercentage_OLD! > 0 else 0""", "PYTHON_9.3")
calculatesubsurfacepercentagenew = arcpy.CalculateField_management(joinoldHOP3fields, newsubsurfacepercentagefield, """!SGSubPercentage_NEW! if !SGSubPercentage_NEW! > 0 else 0""", "PYTHON_9.3")
calculatesubsurfacepercentageold = arcpy.CalculateField_management(joinoldHOP3fields, oldsubsurfacepercentagefield, """!SGSubPercentage_OLD! if !SGSubPercentage_OLD! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ1percentagenew = arcpy.CalculateField_management(joinoldHOP3fields, newEHPZ1percentagefield, """!EHPZ1Percentage_NEW! if !EHPZ1Percentage_NEW! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ1percentageold = arcpy.CalculateField_management(joinoldHOP3fields, oldEHPZ1percentagefield, """!EHPZ1Percentage_OLD! if !EHPZ1Percentage_OLD! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ2percentagenew = arcpy.CalculateField_management(joinoldHOP3fields, newEHPZ2percentagefield, """!EHPZ2Percentage_NEW! if !EHPZ2Percentage_NEW! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ2percentageold = arcpy.CalculateField_management(joinoldHOP3fields, oldEHPZ2percentagefield, """!EHPZ2Percentage_OLD! if !EHPZ2Percentage_OLD! > 0 else 0""", "PYTHON_9.3")
calculateRSZpercentagenew = arcpy.CalculateField_management(joinoldHOP3fields, newRSZpercentagefield, """!RSZPercentage_NEW! if !RSZPercentage_NEW! > 0 else 0""", "PYTHON_9.3")
calculateRSZpercentageold = arcpy.CalculateField_management(joinoldHOP3fields, oldRSZpercentagefield, """!RSZPercentage_OLD! if !RSZPercentage_OLD! > 0 else 0""", "PYTHON_9.3")
calculateHOP1percentagenew = arcpy.CalculateField_management(joinoldHOP3fields, newHOP1percentagefield, """!HOP1Percentage_NEW! if !HOP1Percentage_NEW! > 0 else 0""", "PYTHON_9.3")
calculateHOP1percentageold = arcpy.CalculateField_management(joinoldHOP3fields, oldHOP1percentagefield, """!HOP1Percentage_OLD! if !HOP1Percentage_OLD! > 0 else 0""", "PYTHON_9.3")
calculateHOP2percentagenew = arcpy.CalculateField_management(joinoldHOP3fields, newHOP2percentagefield, """!HOP2Percentage_NEW! if !HOP2Percentage_NEW! > 0 else 0""", "PYTHON_9.3")
calculateHOP2percentageold = arcpy.CalculateField_management(joinoldHOP3fields, oldHOP2percentagefield, """!HOP2Percentage_OLD! if !HOP2Percentage_OLD! > 0 else 0""", "PYTHON_9.3")
calculateHOP3percentagenew = arcpy.CalculateField_management(joinoldHOP3fields, newHOP3percentagefield, """!HOP3Percentage_NEW! if !HOP3Percentage_NEW! > 0 else 0""", "PYTHON_9.3")
calculateHOP3percentageold = arcpy.CalculateField_management(joinoldHOP3fields, oldHOP3percentagefield, """!HOP3Percentage_OLD! if !HOP3Percentage_OLD! > 0 else 0""", "PYTHON_9.3")
calculatesurfaceintegernew = arcpy.CalculateField_management(joinoldHOP3fields, newSGSurIntegerfield, """!SGSurInteger_NEW! if !SGSurInteger_NEW! > 0 else 0""", "PYTHON_9.3")
calculatesurfaceintegerold = arcpy.CalculateField_management(joinoldHOP3fields, oldSGSurIntegerfield, """!SGSurInteger_OLD! if !SGSurInteger_OLD! > 0 else 0""", "PYTHON_9.3")
calculatesubsurfaceintegernew = arcpy.CalculateField_management(joinoldHOP3fields, newSGSubIntegerfield, """!SGSubInteger_NEW! if !SGSubInteger_NEW! > 0 else 0""", "PYTHON_9.3")
calculatesubsurfaceintegerold = arcpy.CalculateField_management(joinoldHOP3fields, oldSGSubIntegerfield, """!SGSubInteger_OLD! if !SGSubInteger_OLD! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ1integernew = arcpy.CalculateField_management(joinoldHOP3fields, newEHPZ1Integerfield, """!EHPZ1Integer_NEW! if !EHPZ1Integer_NEW! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ1integerold = arcpy.CalculateField_management(joinoldHOP3fields, oldEHPZ1Integerfield, """!EHPZ1Integer_OLD! if !EHPZ1Integer_OLD! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ2integernew = arcpy.CalculateField_management(joinoldHOP3fields, newEHPZ2Integerfield, """!EHPZ2Integer_NEW! if !EHPZ2Integer_NEW! > 0 else 0""", "PYTHON_9.3")
calculateEHPZ2integerold = arcpy.CalculateField_management(joinoldHOP3fields, oldEHPZ2Integerfield, """!EHPZ2Integer_OLD! if !EHPZ2Integer_OLD! > 0 else 0""", "PYTHON_9.3")
calculateRSZintegernew = arcpy.CalculateField_management(joinoldHOP3fields, newRSZIntegerfield, """!RSZInteger_NEW! if !RSZInteger_NEW! > 0 else 0""", "PYTHON_9.3")
calculateRSZintegerold = arcpy.CalculateField_management(joinoldHOP3fields, oldRSZIntegerfield, """!RSZInteger_OLD! if !RSZInteger_OLD! > 0 else 0""", "PYTHON_9.3")
calculateHOP1integernew = arcpy.CalculateField_management(joinoldHOP3fields, newHOP1Integerfield, """!HOP1Integer_NEW! if !HOP1Integer_NEW! > 0 else 0""", "PYTHON_9.3")
calculateHOP1integerold = arcpy.CalculateField_management(joinoldHOP3fields, oldHOP1Integerfield, """!HOP1Integer_OLD! if !HOP1Integer_OLD! > 0 else 0""", "PYTHON_9.3")
calculateHOP2integernew = arcpy.CalculateField_management(joinoldHOP3fields, newHOP2Integerfield, """!HOP2Integer_NEW! if !HOP2Integer_NEW! > 0 else 0""", "PYTHON_9.3")
calculateHOP2integerold = arcpy.CalculateField_management(joinoldHOP3fields, oldHOP2Integerfield, """!HOP2Integer_OLD! if !HOP2Integer_OLD! > 0 else 0""", "PYTHON_9.3")
calculateHOP3integernew = arcpy.CalculateField_management(joinoldHOP3fields, newHOP3Integerfield, """!HOP3Integer_NEW! if !HOP3Integer_NEW! > 0 else 0""", "PYTHON_9.3")
calculateHOP3integerold = arcpy.CalculateField_management(joinoldHOP3fields, oldHOP3Integerfield, """!HOP3Integer_OLD! if !HOP3Integer_OLD! > 0 else 0""", "PYTHON_9.3")

print "Intersection, percentage and integer field zero calculation complete"

# Calculate HOP total area field
addnewHOPTotalareafield = arcpy.AddField_management(calculateHOP3integerold, newHOPTotalareafield, FieldType, "",field_alias="HOP Total Area")
calculateHOPTotalareafield = arcpy.CalculateField_management(addnewHOPTotalareafield, newHOPTotalareafield, """!HOP1Area_NEW! + !HOP2Area_NEW! + !HOP3Area_NEW!""", "PYTHON_9.3")

print "HOP total area calculation complete"

# Calculate HOP total percentage field
addnewHOPTotalpercentagefield = arcpy.AddField_management(calculateHOPTotalareafield, newHOPTotalpercentagefield, FieldType, "",field_alias="HOP Percentage Area")
calculatenewHOPTotalpercentagefield = arcpy.CalculateField_management(addnewHOPTotalareafield, newHOPTotalpercentagefield, """100 if !HOPTotalArea!/ !Total_LOP_Area!*100 > 100 else !HOPTotalArea!/ !Total_LOP_Area!*100""", "PYTHON_9.3")

print "HOP total percentage calculation complete"

# Calculate In HOP field
addInHOPfield = arcpy.AddField_management(calculatenewHOPTotalpercentagefield, InHOPfield, FieldType, "",field_alias="In HOP")
calculateInHOPfield = arcpy.CalculateField_management(addInHOPfield, InHOPfield, """1 if !HOPTotalArea! > 0 else 0""", "PYTHON_9.3")

print "In HOP calculation complete"

# Calculate No Zone field
addnewNoZonefield = arcpy.AddField_management(calculateInHOPfield, NewNoZonefield, FieldType, "",field_alias="No Zone New")
calculateNewNoZonefield = arcpy.CalculateField_management(addnewNoZonefield, NewNoZonefield, """1 if sum([ !SGSurArea_NEW!, !SGSubArea_NEW!, !EHPZ1Area_NEW!, !EHPZ2Area_NEW!, !RSZArea_NEW!, !HOP1Area_NEW!, !HOP2Area_NEW!, !HOP3Area_NEW!]) < 1 else 0""", "PYTHON_9.3")
addoldNoZonefield = arcpy.AddField_management(calculateNewNoZonefield, OldNoZonefield, FieldType, "",field_alias="No Zone Old")
calculateOldNoZonefield = arcpy.CalculateField_management(addoldNoZonefield, OldNoZonefield, """1 if sum([ !SGSurArea_OLD!, !SGSubArea_OLD!, !EHPZ1Area_OLD!, !EHPZ2Area_OLD!, !RSZArea_OLD!, !HOP1Area_OLD!, !HOP2Area_OLD!, !HOP3Area_OLD!]) < 1 else 0""", "PYTHON_9.3")

print "No zone calculation complete"

# Calculate address intersections
addcontainsaddress = arcpy.AddField_management(calculateOldNoZonefield, AddressPresentField, "Text", "",field_alias="Contains Address")
intersectPolyAddress = arcpy.Intersect_analysis([addcontainsaddress,AddressPoly], str(Working)+"\Parcel_LOPABPPolyintersect", "ALL", "", "INPUT")
dissolvePolyAddress = arcpy.Dissolve_management(intersectPolyAddress, str(Working)+"\Parcel_LOPABPPolyDissolve", LOPField, "", "", "")
addpolyaddressfield = arcpy.AddField_management(dissolvePolyAddress, "PolyAddress", "TEXT", "",field_alias="Contains Poly Address")
calculatepolyaddressfield = arcpy.CalculateField_management(addpolyaddressfield, "PolyAddress", """'Yes'""", "PYTHON_9.3")
intersectNonPolyAddress = arcpy.Intersect_analysis([addcontainsaddress,AddressNonPoly], str(Working)+"\Parcel_LOPABPNonPolyintersect", "ALL", "", "INPUT")
dissolveNonPolyAddress = arcpy.Dissolve_management(intersectNonPolyAddress, str(Working)+"\Parcel_LOPABPNonPolyDissolve", LOPField, "", "", "")
addnonpolyaddressfield = arcpy.AddField_management(dissolveNonPolyAddress, "NonPolyAddress", "TEXT", "",field_alias="Contains Non-Poly Address")
calculatenonpolyaddressfield = arcpy.CalculateField_management(addnonpolyaddressfield, "NonPolyAddress", """'Yes'""", "PYTHON_9.3")
joinPolyABP = arcpy.JoinField_management(addcontainsaddress, LOPField, calculatepolyaddressfield, LOPField, "PolyAddress")
joinNonPolyABP = arcpy.JoinField_management(joinPolyABP, LOPField, calculatenonpolyaddressfield, LOPField, "NonPolyAddress")
calculatecontainsaddress = arcpy.CalculateField_management(joinNonPolyABP, "Contains_Address", """'Yes' if !PolyAddress! == 'Yes' or !NonPolyAddress! == 'Yes' else 'No'""", "PYTHON_9.3")
deleteAddressfields = arcpy.DeleteField_management(calculatecontainsaddress,["PolyAddress","NonPolyAddress"])

print "Contains address calculation complete"

# Local Authority calculations
localauthorityintersect = arcpy.Intersect_analysis([deleteAddressfields,LocalAuthority], str(Working)+"\Parcel_LocalAuthorityIntersect", "ALL", "", "INPUT")
localauthoritydissolve = arcpy.Dissolve_management(localauthorityintersect, str(Working)+"\Parcel_LocalAuthorityDissolve", [LOPField,"lad17nm"], "", "", "")
localauthoritysummarystats = arcpy.Statistics_analysis(localauthoritydissolve, str(Working)+"\Parcel_LocalAuthoritySummaryStats", "OwnershipReferenceNumber COUNT","OwnershipReferenceNumber")
lamaxvalue = float('-inf')
lafc = localauthoritysummarystats
lamaxvalfield = "COUNT_OwnershipReferenceNumber"
with arcpy.da.SearchCursor(lafc, lamaxvalfield) as cursor:
    for row in cursor:
        value = row[0]
        if value > lamaxvalue:
            lamaxvalue = value
for i in range(lamaxvalue):
    addlafields = arcpy.AddField_management(calculateOldNoZonefield, "LocalAuthority_"+str(i+1), "TEXT", "",field_alias="Local Authority "+str(i+1))

print "Local Authority field addition complete"

# Add field to concatenate to
addconclafield = arcpy.AddField_management(localauthoritydissolve, "ConcatenatedLA", "TEXT", "",field_alias="Concatenated Local Authority")
# Set concatenate la parameters
Delimiter = ","
laReadFromField = "lad17nm"
# Create an empty ladictionary.
ladictionary = {}
# Create a variable and set its value to the last row value. The first one is -1 which means no row before the first.
lastid = -1
# Create an empty variable which will store the value of the last row in the code below.
lastvalue = ""
# Insert Search cursor on a feature class or table to iterate through row objects and extract field values.
cur1 = arcpy.SearchCursor(localauthoritydissolve, "", "", "", LOPField +" A;" + laReadFromField +" A")

for row in cur1:
    id = row.getValue(LOPField)
    value = row.getValue(laReadFromField)
    ladictionary[id] = value
    if id == lastid:
        value = str(lastvalue) + Delimiter + str(value)
        ladictionary[id] = value
    lastid = id
    lastvalue = value
del cur1, row

# Insert Update cursor to update or delete rows on the specified feature class, shapefile, or table.
cur2 = arcpy.UpdateCursor(localauthoritydissolve)
for row in cur2:
    id = row.getValue(LOPField)
    row.setValue("ConcatenatedLA", ladictionary[id])
    cur2.updateRow(row)
del cur2, row

localauthoritydissolve2 = arcpy.Dissolve_management(localauthoritydissolve, str(Working)+"\Parcel_LocalAuthorityDissolveMerge", [LOPField,"ConcatenatedLA"], "", "", "")
joinConcatenatedLA = arcpy.JoinField_management(requiredLOP, LOPField, localauthoritydissolve2, LOPField, "ConcatenatedLA")

# IF MORE THAN 3 LOCAL AUTHORITIES EXIST WITHIN REQUIRED LOP, THE CALCULTIONS BELOW WILL NEED TO BE AMENDED TO INCLUDE THE ADDITIONAL FIELD CALCULATIONS
lafieldnames = [f.name for f in arcpy.ListFields(requiredLOP,"LocalAuthority*")]

# Calculate Local Authority fields
calculatela1 = arcpy.CalculateField_management(requiredLOP, lafieldnames[0], """!ConcatenatedLA!.split(",")[0]""", "PYTHON_9.3")
#calculatela2 = arcpy.CalculateField_management(requiredLOP, lafieldnames[1], """!ConcatenatedLA!.split(",")[1] if "," in !ConcatenatedLA! else None""", "PYTHON_9.3")
#calculatela3 = arcpy.CalculateField_management(requiredLOP, lafieldnames[2], """!ConcatenatedLA!.split(",")[-1] if "," in !ConcatenatedLA! else None""", "PYTHON_9.3")
#recalculatela3 = arcpy.CalculateField_management(requiredLOP, lafieldnames[2], """None if !LocalAuthority_2! == !LocalAuthority_3! else !LocalAuthority_3!""", "PYTHON_9.3")
#deleteconclafield = arcpy.DeleteField_management(requiredLOP,["ConcatenatedLA"])

print "Local Authority calculation complete"

# Constituency calculations
constituencyintersect = arcpy.Intersect_analysis([calculatela1,Constituency], str(Working)+"\Parcel_constituencyIntersect", "ALL", "", "INPUT")
constituencydissolve = arcpy.Dissolve_management(constituencyintersect, str(Working)+"\Parcel_constituencyDissolve", [LOPField,"pcon15nm"], "", "", "")
constituencysummarystats = arcpy.Statistics_analysis(constituencydissolve, str(Working)+"\Parcel_constituencySummaryStats", "OwnershipReferenceNumber COUNT","OwnershipReferenceNumber")
cmaxvalue = float('-inf')
cfc = constituencysummarystats
cmaxvalfield = "COUNT_OwnershipReferenceNumber"
with arcpy.da.SearchCursor(cfc, cmaxvalfield) as cursor:
    for row in cursor:
        value = row[0]
        if value > cmaxvalue:
            cmaxvalue = value
for i in range(cmaxvalue):
    addcfields = arcpy.AddField_management(calculateOldNoZonefield, "Constituency_"+str(i+1), "TEXT", "",field_alias="Constituency "+str(i+1))

print "Constituency field addition complete"

# Add field to concatenate to
addconclafield = arcpy.AddField_management(constituencydissolve, "ConcatenatedC", "TEXT", "",field_alias="Concatenated Constituency")
# Set concatenate c parameters
Delimiter = ","
cReadFromField = "pcon15nm"
# Create an empty cdictionary.
cdictionary = {}
# Create a variable and set its value to the last row value. The first one is -1 which means no row before the first.
lastid = -1
# Create an empty variable which will store the value of the last row in the code below.
lastvalue = ""
# Insert Search cursor on a feature class or table to iterate through row objects and extract field values.
cur1 = arcpy.SearchCursor(constituencydissolve, "", "", "", LOPField +" A;" + cReadFromField +" A")

for row in cur1:
    id = row.getValue(LOPField)
    value = row.getValue(cReadFromField)
    cdictionary[id] = value
    if id == lastid:
        value = str(lastvalue) + Delimiter + str(value)
        cdictionary[id] = value
    lastid = id
    lastvalue = value
del cur1, row

# Insert Update cursor to update or delete rows on the specified feature class, shapefile, or table.
cur2 = arcpy.UpdateCursor(constituencydissolve)
for row in cur2:
    id = row.getValue(LOPField)
    row.setValue("ConcatenatedC", cdictionary[id])
    cur2.updateRow(row)
del cur2, row

constituencydissolve2 = arcpy.Dissolve_management(constituencydissolve, str(Working)+"\Parcel_constituencyDissolveMerge", [LOPField,"ConcatenatedC"], "", "", "")
joinConcatenatedC = arcpy.JoinField_management(requiredLOP, LOPField, constituencydissolve2, LOPField, "ConcatenatedC")

# IF MORE THAN 3 LOCAL AUTHORITIES EXIST WITHIN REQUIRED LOP, THE CALCULTIONS BELOW WILL NEED TO BE AMENDED TO INCLUDE THE ADDITIONAL FIELD CALCULATIONS
cfieldnames = [f.name for f in arcpy.ListFields(requiredLOP,"Constituency*")]

# Calculate Constituency fields
calculatec1 = arcpy.CalculateField_management(requiredLOP, cfieldnames[0], """!ConcatenatedC!.split(",")[0]""", "PYTHON_9.3")
#calculatec2 = arcpy.CalculateField_management(requiredLOP, cfieldnames[1], """!ConcatenatedC!.split(",")[1] if "," in !ConcatenatedC! else None""", "PYTHON_9.3")
#calculatec3 = arcpy.CalculateField_management(requiredLOP, cfieldnames[2], """!ConcatenatedC!.split(",")[-1] if "," in !ConcatenatedC! else None""", "PYTHON_9.3")
#recalculatec3 = arcpy.CalculateField_management(requiredLOP, cfieldnames[2], """None if !Constituency_2! == !Constituency_3! else !Constituency_3!""", "PYTHON_9.3")
#deleteconccfield = arcpy.DeleteField_management(requiredLOP,["ConcatenatedC"])

print "Constituency calculation complete"

# Calculate Scenario field
addscenariofield = arcpy.AddField_management(calculatec1, scenario, FieldType, "",field_alias="Scenario")
addscenariotextfield = arcpy.AddField_management(addscenariofield, scenariotext, "TEXT", "",field_length = 500, field_alias="Scenario Text")
addgisreviewfield = arcpy.AddField_management(addscenariotextfield, gisreview, "TEXT", "",field_length = 500, field_alias="GIS Comment")
addexclusionfield = arcpy.AddField_management(addgisreviewfield, exclusion, "TEXT", "",field_length = 500, field_alias="Exclusion Reason")
addHOPScenariofield = arcpy.AddField_management(addexclusionfield, HOPScenario, FieldType, "",field_alias="HOP Scenario")
addHOPScenariotextfield = arcpy.AddField_management(addHOPScenariofield, HOPScenariotext, "TEXT", "",field_length = 500, field_alias="HOP Scenario Text")

# Calculate Scenario field
with arcpy.da.UpdateCursor(calculatec1, [newsurfaceareafield,oldsurfaceareafield,newsubsurfaceareafield,oldsubsurfaceareafield,newEHPZ1areafield,oldEHPZ1areafield,newEHPZ2areafield,oldEHPZ2areafield,newRSZareafield,oldRSZareafield,newHOP1areafield,oldHOP1areafield,newHOP2areafield,oldHOP2areafield,newHOP3areafield,oldHOP3areafield,AddressPresentField,scenario,scenariotext,gisreview,exclusion,HOPScenario,HOPScenariotext]) as cursor:
    for row in cursor:
        # SCENARIOS DEALING WITH CHANGE
        # Scenario 1 Land with and without an address within it and within 2019 Surface Safeguarding where the zone area has increased
        if (row[0] - row[1] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
            row[17] = 1
            row[18] = 'Within January 2019 Surface Safeguarding only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
        # Scenario 2 Land with and without an address within it and within 2019 Surface Safeguarding where the zone area has decreased
        if (row[1] - row[0] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
            row[17] = 2
            row[18] = 'Within January 2019 Surface Safeguarding only, where Surface Safeguarding has decreased by greater than or equal to 1sqm'
        # Scenario 3 Land with and without an address within it and within 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 1 where the Surface Safeguarding zone area has increased
        if (row[0] - row[1] >=1 and row[0] > 1 and row[2] < 1 and row[4] > 1 and row[6] < 1 and row[8] < 1):
            row[17] = 3
            row[18] = 'Within January 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 1 only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
        # Scenario 4 Land with and without an address within it and within 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 1 where the Surface Safeguarding zone area has decreased
##        if (row[1] - row[0] >=1 and row[0] > 1 and row[2] < 1 and row[4] > 1 and row[6] < 1 and row[8] < 1):
##            row[17] = 4
##            row[18] = 'Within January 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 1 only, where Surface Safeguarding has decreased by greater than or equal to 1sqm'
        # Scenario 4 Land with and without an address within it and within 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 2 where the Surface Safeguarding zone area has increased
        if (row[0] - row[1] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] > 1 and row[8] < 1):
            row[17] = 4
            row[18] = 'Within January 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 2 only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
        # Scenario 5 Land with and without an address within it and within 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 2 where the Surface Safeguarding zone area has increased
        if (row[1] - row[0] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] > 1 and row[8] < 1):
            row[17] = 5
            row[18] = 'Within January 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 2 only, where Surface Safeguarding has decreased by greater than or equal to 1sqm'
        # Scenario 6 Land with and without an address within it and within 2019 Surface Safeguarding and Rural Support Zone where the Surface Safeguarding zone area has increased
        if (row[16] == 'Yes' and row[0] - row[1] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] > 1):
            row[17] = 6
            row[18] = 'Within January 2019 Surface Safeguarding and Rural Support Zone only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
        if (row[16] == 'No' and row[0] - row[1] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] > 1):
            row[17] = 1
            row[18] = 'Within January 2019 Surface Safeguarding only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
            row[19] = 'Was Scenario 6 due to intersection with Rural Support Zone but moved to Scenario 1 as no address is present within the Parcel and the Safeguarding Zone intersection has increased by greater than or equal to 1sqm'
       # Scenario 7 Land with and without an address within it and within 2019 Surface Safeguarding and Rural Support Zone where the Surface Safeguarding zone area has decreased
        if (row[16] == 'Yes' and row[1] - row[0] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] > 1):
            row[17] = 7
            row[18] = 'Within January 2019 Surface Safeguarding and Rural Support Zone only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
        if (row[16] == 'No' and row[1] - row[0] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] > 1):
            row[17] = 2
            row[18] = 'Within January 2019 Surface Safeguarding only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
            row[19] = 'Was Scenario 7 due to intersection with Rural Support Zone but moved to Scenario 2 as no address is present within the Parcel and the Safeguarding Zone intersection has decreased by greater than or equal to 1sqm'
       # Scenario 8 Land with and without an address within it and within 2019 Surface Safeguarding, Enhanced Homeowner Protection Zone 1 and Rural Support Zone where the Surface Safeguarding zone area has increased
        if (row[16] == 'Yes' and row[0] - row[1] >=1 and row[0] > 1 and row[2] < 1 and row[4] > 1 and row[6] < 1 and row[8] > 1):
            row[17] = 8
            row[18] = 'Within January 2019 Surface Safeguarding, Enhanced Homeowner Protection Zone 1 and Rural Support Zone only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
        if (row[16] == 'No' and row[0] - row[1] >=1 and row[0] > 1 and row[2] < 1 and row[4] > 1 and row[6] < 1 and row[8] > 1):
            row[17] = 3
            row[18] = 'Within January 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 1 only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
            row[19] = 'Was Scenario 8 due to intersection with Rural Support Zone but moved to Scenario 3 as no address is present within the Parcel and the Safeguarding Zone intersection has increased by greater than or equal to 1sqm'
       # Scenario 9 Land with and without an address within it and within 2019 Surface Safeguarding, Enhanced Homeowner Protection Zone 1 and Rural Support Zone where the Surface Safeguarding zone area has increased
        if (row[16] == 'Yes' and row[1] - row[0] >=1 and row[0] > 1 and row[2] < 1 and row[4] > 1 and row[6] < 1 and row[8] > 1):
            row[17] = 9
            row[18] = 'Within January 2019 Surface Safeguarding, Enhanced Homeowner Protection Zone 1 and Rural Support Zone only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
##        if (row[16] == 'No' and row[1] - row[0] >=1 and row[0] > 1 and row[2] < 1 and row[4] > 1 and row[6] < 1 and row[8] > 1):
##            row[17] = 4
##            row[18] = 'Within January 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 1 only, where Surface Safeguarding has decreased by greater than or equal to 1sqm'
##            row[19] = 'Was Scenario 10 due to intersection with Rural Support Zone but moved to Scenario 4 as no address is present within the Parcel and the Safeguarding Zone intersection has decreased by greater than or equal to 1sqm'
       # Scenario 10 Land with and without an address within it and within 2019 Surface Safeguarding, Enhanced Homeowner Protection Zone 2 and Rural Support Zone where the Surface Safeguarding zone area has increased
        if (row[16] == 'Yes' and row[0] - row[1] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] > 1 and row[8] > 1):
            row[17] = 10
            row[18] = 'Within January 2019 Surface Safeguarding, Enhanced Homeowner Protection Zone 2 and Rural Support Zone only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
        if (row[16] == 'No' and row[0] - row[1] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] > 1 and row[8] > 1):
            row[17] = 4
            row[18] = 'Within January 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 2 only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
            row[19] = 'Was Scenario 10 due to intersection with Rural Support Zone but moved to Scenario 4 as no address is present within the Parcel and the Safeguarding Zone intersection has increased by greater than or equal to 1sqm'
       # Scenario 11 Land with and without an address within it and within 2019 Surface Safeguarding, Enhanced Homeowner Protection Zone 2 and Rural Support Zone where the Surface Safeguarding zone area has increased
        if (row[16] == 'Yes' and row[1] - row[0] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] > 1 and row[8] > 1):
            row[17] = 11
            row[18] = 'Within January 2019 Surface Safeguarding, Enhanced Homeowner Protection Zone 2 and Rural Support Zone only, where Surface Safeguarding has increased by greater than or equal to 1sqm'
        if (row[16] == 'No' and row[1] - row[0] >=1 and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] > 1 and row[8] > 1):
            row[17] = 6
            row[18] = 'Within January 2019 Surface Safeguarding and Enhanced Homeowner Protection Zone 2 only, where Surface Safeguarding has decreased by greater than or equal to 1sqm'
            row[19] = 'Was Scenario 11 due to intersection with Rural Support Zone but moved to Scenario 5 as no address is present within the Parcel and the Safeguarding Zone intersection has decreased by greater than or equal to 1sqm'
        # Scenario 12 Land with and without an address within it and within 2019 Enhanced Homeowner Protection Zone 2
        if (row[0] < 1 and row[2] < 1 and row[4] < 1 and row[6] > 1 and row[8] < 1):
            row[17] = 12
            row[18] = 'Within January 2019 Enhanced Homeowner Protection Zone 2'
       # Scenario 14 Land with and without an address within it and within 2019 Enhanced Homeowner Protection Zone 2 and Rural Support Zone
##        if (row[16] == 'Yes' and row[0] < 1 and row[2] < 1 and row[4] < 1 and row[6] > 1 and row[8] > 1):
##            row[17] = 14
##            row[18] = 'Within January 2019 Enhanced Homeowner Protection Zone 2 and Rural Support Zone only'
##        if (row[16] == 'No' and row[0] < 1 and row[2] < 1 and row[4] < 1 and row[6] > 1 and row[8] > 1):
##            row[17] = 13
##            row[18] = 'Within January 2019 Enhanced Homeowner Protection Zone 2'
##            row[19] = 'Was Scenario 14 due to intersection with Rural Support Zone but moved to Scenario 13 as no address is present within the Parcel'
       # Scenario 13 Land with and without an address within it and within 2019 Surface Safeguarding and Subsurface Safeguarding where the Safeguarding zone area has changed
        if (((row[0] - row[1] >=1 or row[1] - row[0] >=1) or (row[2] - row[3] >=1 or row[3] - row[2] >=1)) and row[0] > 1 and row[2] > 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
            row[17] = 13
            row[18] = 'Within January 2019 Surface Safeguarding and Subsurface Safeguarding only, where Surface Safeguarding or Subsurface Safeguarding has changed'
        if ((row[0] - row[1] >=1 or row[1] - row[0] >=1) and row[0] > 1 and row[2] > 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
            row[19] = 'Change is within Surface Safeguarding'
        if ((row[2] - row[3] >=1 or row[3] - row[2] >=1) and row[0] > 1 and row[2] > 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
            row[19] = 'Change is within Subsurface Safeguarding'
       # Scenario 16 Land with and without an address within it and within 2017 Surface Safeguarding and now within 2019 Subsurface Safeguarding
##        if (row[1] > 1 and row[0] < 1 and row[2] > 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
##            row[17] = 16
##            row[18] = 'Was within 2017 Surface Safeguarding and now within 2019 Subsurface Safeguarding'
        # Scenario 14 Land within January 2019 Subsurface Safeguarding only, where Subsurface Safeguarding has increased or decreased by greater than or equal to 1sqm
        if ((row[2] - row[3] >=1 or row[3] - row[2] >=1) and row[0] < 1 and row[2] > 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
            row[17] = 14
            row[18] = 'Within January 2019 Subsurface Safeguarding only, where Subsurface Safeguarding has increased or decreased by greater than or equal to 1sqm'
        if ((row[2] - row[3] >=1 or row[3] - row[2] >=1) and row[0] > 1 and row[2] > 1 and row[3] == 0 and row[4] < 1 and row[6] < 1 and row[8] < 1):
            row[19] = 'The Parcel is newly in Subsurface Safeguarding'
        # Scenario 18 Land within January 2019 Subsurface Safeguarding and Rural Support Zone only, where Subsurface Safeguarding has increased or decreased by greater than or equal to 1sqm
##        if (row[16] == 'Yes' and (row[2] - row[3] >=1 or row[3] - row[2] >=1) and row[0] < 1 and row[2] > 1 and row[4] < 1 and row[6] < 1 and row[8] > 1):
##            row[17] = 18
##            row[18] = 'Within January 2019 Subsurface Safeguarding only, where Subsurface Safeguarding has increased or decreased by greater than or equal to 1sqm'
##        if (row[16] == 'No' and (row[2] - row[3] >=1 or row[3] - row[2] >=1) and row[0] < 1 and row[2] > 1 and row[4] < 1 and row[6] < 1 and row[8] > 1):
##            row[17] = 17
##            row[18] = 'Within January 2019 Subsurface Safeguarding only, where Subsurface Safeguarding has increased or decreased by greater than or equal to 1sqm'
##            row[19] = 'Was Scenario 18 due to intersection with Rural Support Zone but moved to Scenario 17 as no address is present within the Parcel'
       # Scenario 15 Land previously within Surface Safeguarding and now in No Zones
        if (row[1] > 1 and row[0] < 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
            row[17] = 15
            row[18] = 'Previously within Surface Safeguarding and in No Zone in January 2019'
        # Scenario 20 Land containing an address and previously within RSZ and now in No Zones
##        if (row[16] == 'Yes' and row[9] > 1 and row[0] < 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
##            row[17] = 20
##            row[18] = 'Previously within Rural Support Zone and containing an address and in No Zone in January 2019'
        # Scenario 16 Land containing an address and previously within HOP and now in No Zones
        if (row[16] == 'Yes' and (row[11] > 1 or row[13] > 1 or row[15] > 1) and row[0] < 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] < 1 and row[10] < 1 and row[12] < 1 and row[14] < 1):
            row[17] = 16
            row[18] = 'Previously within HOP and containing an address and in No Zone in January 2019'
        # SCENARIOS WHERE THERE HAS BEEN NO CHANGE
        # Scenario 17 Land previously within Rural Support Zone and within January 2019 Rural Support Zone only
        if (row[16] == 'Yes' and row[8] - row[9] <=1 and row[9] - row[8] <=1 and row[0] < 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] >= 1 and row[9] >= 1):
            row[17] = 17
            row[18] = 'Within January 2019 Rural Support Zone and containing an address, and no impactful change between this area value and July 2017 Rural Support Zone'
        if (row[16] == 'No' and row[8] - row[9] <=1 and row[9] - row[8] <=1 and row[0] < 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] >= 1 and row[9] >= 1):
            row[17] = 17
            row[18] = 'Within January 2019 Rural Support Zone and without an address, and no impactful change between this area value and July 2017 Rural Support Zone'
        # Scenario 18 Land previously within Surface Safeguarding and within January 2019 Surface Safeguarding only
        if (row[0] - row[1] <= 1 and row[1] - row[0] <= 1 and row[0] >= 1 and row[1] >= 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
            row[17] = 18
            row[18] = 'Within January 2019 Surface Safeguarding Zone, and no impactful change between this area value and July 2017 Surface Safeguarding Zone'
        # Scenario 19 Land previously within Surface Safeguarding and Rural Support Zone and within January 2019 Rural Support Zone only
        if (row[16] == 'Yes' and row[0] - row[1] <= 1 and row[1] - row[0] <= 1 and row[0] >= 1 and row[1] >= 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] - row[9] <= 1 and row[9] - row[8] <= 1 and row[8] >= 1 and row[9] >= 1):
            row[17] = 19
            row[18] = 'Within January 2019 Surface Safeguarding and Rural Support Zone and no impactful change between this area value and July 2017 Surface Safeguarding Rural Support Zone'
        if (row[16] == 'No' and row[0] - row[1] <= 1 and row[1] - row[0] <= 1 and row[0] >= 1 and row[1] >= 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[8] - row[9] <= 1 and row[9] - row[8] <= 1 and row[8] >= 1 and row[9] >= 1):
            row[17] = 18
            row[18] = 'Within January 2019 Surface Safeguarding Zone, and no impactful change between this area value and July 2017 Surface Safeguarding Zone'
            row[19] = 'Was Scenario 19 due to intersection with Rural Support Zone but moved to Scenario 18 as no address is present within the Parcel'
        # Scenario 20 Land previously within Surface Safeguarding and within January 2019 Surface Safeguarding only
        if (row[2] - row[3] <= 1 and row[3] - row[2] <= 1 and row[0] < 1 and row[1] < 1 and row[2] >= 1 and row[3] >= 1 and row[4] < 1 and row[6] < 1 and row[8] < 1):
            row[17] = 20
            row[18] = 'Within January 2019 Subsurface Safeguarding Zone, and no impactful change between this area value and July 2017 Subsurface Safeguarding Zone'
        # Scenario 26 Land previously within Surface Safeguarding and Rural Support Zone and within January 2019 Rural Support Zone only
##        if (row[16] == 'Yes' and row[2] - row[3] <= 1 and row[3] - row[2] <= 1 and row[0] < 1 and row[2] >= 1 and row[3] >= 1 and row[4] < 1 and row[6] < 1 and row[8] - row[9] <= 1 and row[9] - row[8] <= 1 and row[8] >= 1 and row[9] >= 1):
##            row[17] = 26
##            row[18] = 'Within January 2019 Subsurface Safeguarding and Rural Support Zone and no impactful change between this area value and July 2017 Subsurface Safeguarding and Rural Support Zone'
##        if (row[16] == 'No' and row[2] - row[3] <= 1 and row[3] - row[2] <= 1 and row[0] < 1 and row[2] >= 1 and row[3] >= 1 and row[4] < 1 and row[6] < 1 and row[8] - row[9] <= 1 and row[9] - row[8] <= 1 and row[8] >= 1 and row[9] >= 1):
##            row[17] = 25
##            row[18] = 'Within January 2019 Subsurface Safeguarding Zone, and no impactful change between this area value and July 2017 Subsurface Safeguarding Zone'
##            row[19] = 'Was Scenario 26 due to intersection with Rural Support Zone but moved to Scenario 25 as no address is present within the Parcel'
        # Scenario 21 Land previously within Enhanced Homeowner Protection Zone 1 and within January 2019 Enhanced Homeowner Protection Zone 1 only
        if (row[4] - row[5] <= 1 and row[5] - row[4] <= 1 and row[0] < 1 and row[2] < 1 and row[4] >= 1 and row[5] >= 1 and row[6] < 1 and row[8] < 1):
            row[17] = 21
            row[18] = 'Within July 2017 Enhanced Homeowner Protection Zone 1 and RSZ, and now within January 2019 Enhanced Homeowner Protection Zone 1 only'
        # Scenario 22 Land previously within Enhanced Homeowner Protection Zone 1 and Rural Support Zone and within January 2019 Enhanced Homeowner Protection Zone 1 and Rural Support Zone only
        if (row[16] == 'Yes' and row[4] - row[5] <= 1 and row[5] - row[4] <= 1 and row[0] < 1 and row[2] < 1 and row[4] >= 1 and row[5] >= 1 and row[6] < 1 and row[8] - row[9] <= 1 and row[9] - row[8] <= 1 and row[8] >= 1 and row[9] >= 1):
            row[17] = 22
            row[18] = 'Within January 2019 Enhanced Homeowner Protection Zone 1 and Rural Support Zone and no impactful change between this area value and July 2017 Enhanced Homeowner Protection Zone 1 and Rural Support Zone'
        if (row[16] == 'No' and row[2] - row[3] <= 1 and row[3] - row[2] <= 1 and row[0] < 1 and row[2] >= 1 and row[3] >= 1 and row[4] < 1 and row[6] < 1 and row[8] - row[9] <= 1 and row[9] - row[8] <= 1 and row[8] >= 1 and row[9] >= 1):
            row[17] = 21
            row[18] = 'Within January 2019 Enhanced Homeowner Protection Zone 1, and no impactful change between this area value and July 2017 Enhanced Homeowner Protection Zone 1'
            row[19] = 'Was Scenario 22 due to intersection with Rural Support Zone but moved to Scenario 21 as no address is present within the Parcel'
        # Scenario 23 Land and addresses within January 2019 HOP
        if (row[16] == 'Yes' and (row[10] > 1 or row[12] > 1 or row[14] > 1)):
            row[21] = 23
            row[22] = 'Within January 2019 Homeowner Protection Zones'
        if (row[16] == 'No' and (row[10] > 1 or row[12] > 1 or row[14] > 1)):
            row[21] = 23
            row[22] = 'Within January 2019 Homeowner Protection Zones but no dwelling'
        # Scenario 24 Excluded from Scenarios because intersections with all zones are less than 1sqm so likely slivers
        if (row[0] < 1 and row[1] < 1 and row[2] < 1 and row[3] < 1 and row[4] < 1 and row[5] < 1 and row[6] < 1 and row[7] < 1 and row[8] < 1 and row[9] < 1 and row[10] < 1 and row[11] < 1 and row[12] < 1 and row[13] < 1 and row[14] < 1 and row[15] < 1):
            row[17] = 24
            row[18] = 'Excluded'
            row[19] = 'Excluded from Scenarios because intersections with all zones are less than 1sqm so likely slivers'
        # Scenario 25 Land with a decrease in RSZ between 2017 and 2019 and where Surface Safeguarding has not changed
        if (row[0] == row[1] and row[0] > 1 and row[2] < 1 and row[4] < 1 and row[6] < 1 and row[9] - row[8] >= 1 and row[8] > 1):
            row[17] = 25
            row[18] = 'Within January 2019 Surface Safeguarding only, where Surface Safeguarding has not changed but RSZ has decreased'
        # Scenario 26 In Surface, EHPZ1 and RSZ 2017 and 2019, no change
        if (row[0] - row[1] <= 1 and row[1] - row[0] <= 1 and row[0] > 1 and row[4] - row[5] <= 1 and row[4] > 1 and row[5] - row[4] <= 1 and row[8] - row[9] <= 1 and row[9] - row[8] <= 1 and row[8] > 1 and row[2] < 1 and row[6] < 1):
            row[17] = 26
            row[18] = 'Within January 2019 Surface Safeguarding, Enhanced Homeowner Protection Zone 1 and Rural Support Zone and no impactful change between this and July 2017 Surface Safeguarding, Enhanced Homeowner Protection Zone 1 and Rural Support Zone'
        cursor.updateRow(row)
print "Scenarios calculated"

#Capture end time of script
print 'Safeguarding finished in: %s\n\n' % (datetime.now() - start)
