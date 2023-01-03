# File name: GSSGISK-2236_Finalise_HS2B_2020_Safeguarding_Script_Manchester.py
# Author: Ollie Brown
# Date created: 20200312
# Date last modified: N/A
# Python Version: 2.7.13

# Import system modules
import arcpy
from datetime import *
from collections import Counter
import operator
import pprint

#Capture start time of script  
start = datetime.now()  
print 'Safeguarding Started: %s\n' % (start)  

# Set global variables
arcpy.env.overwriteOutput = True

# Change the workspace to where you would like the Project folder to be saved
workspace = r"C:\Users\ukodb001\Desktop\Tasks\2020\GSSGISK-2236_Finalise_HS2B_2020_Safeguarding_Script\ScriptRun\Manchester"

# Change the name of the folder to the Project name  
projectname = "HS2B_Safeguarding_2020_Manchester"

# Create a container folder within the specified workspace containing the folder specified as Project Name above and dated to current date time
createprojectfolder = arcpy.CreateFolder_management(workspace, projectname+"_"+str(datetime.today().strftime('%Y%m%d_%H%M%S')))

# Create required FGDBs for Output and Working data
Output = arcpy.CreateFileGDB_management(createprojectfolder,"Output.gdb")
Working = arcpy.CreateFileGDB_management(createprojectfolder,"Working.gdb")

# Set local variables
LOPField = "OwnershipReferenceNumber"
LocalAuthorityField = "lad17nm"
ConstituencyField = "pcon15nm"
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
newEHPZ3areafield = "EHPZ3Area_NEW"
oldEHPZ3areafield = "EHPZ3Area_OLD"
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
newEHPZ3percentagefield = "EHPZ3Percentage_NEW"
oldEHPZ3percentagefield = "EHPZ3Percentage_OLD"
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
newEHPZ3Integerfield = "EHPZ3Integer_NEW"
oldEHPZ3Integerfield = "EHPZ3Integer_OLD"
newRSZIntegerfield = "RSZInteger_NEW"
oldRSZIntegerfield = "RSZInteger_OLD"
newHOP1Integerfield = "HOP1Integer_NEW"
oldHOP1Integerfield = "HOP1Integer_OLD"
newHOP2Integerfield = "HOP2Integer_NEW"
oldHOP2Integerfield = "HOP2Integer_OLD"
newHOP3Integerfield = "HOP3Integer_NEW"
oldHOP3Integerfield = "HOP3Integer_OLD"
newHOPTotalareafield = "HOPTotalArea_NEW"
oldHOPTotalareafield = "HOPTotalArea_OLD"
newHOPTotalpercentagefield = "HOPTotalPercentage_NEW"
oldHOPTotalpercentagefield = "HOPTotalPercentage_OLD"
newInHOPfield = "In_HOP_NEW"
oldInHOPfield = "In_HOP_OLD"
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
HMLRTitles = r"C:\Users\ukodb001\Desktop\Tasks\2020\GSSGISK-2236_Finalise_HS2B_2020_Safeguarding_Script\Incoming\SG_Input\Raw.gdb\HMLR_Parcels"
LandOwnershipParcels = r"C:\Users\ukodb001\Desktop\Tasks\2020\GSSGISK-2236_Finalise_HS2B_2020_Safeguarding_Script\Incoming\SG_Input\Raw.gdb\Safeguarding_Land_Ownership_Parcels"
NewSafeguardingZones = r"C:\Users\ukodb001\Desktop\Tasks\2020\GSSGISK-2236_Finalise_HS2B_2020_Safeguarding_Script\Incoming\2C864-MCL-GI-GDD-000-000003_P07\2C864-MCL-GI-GDD-000-000003_P07\Y20W10.gdb\HS2_HSTWO_SafeguardingAndZonedPropertySchemes_Ply"
OldSafeguardingZones = r"C:\Users\ukodb001\Desktop\Tasks\2020\GSSGISK-2236_Finalise_HS2B_2020_Safeguarding_Script\Incoming\GIS_Data_Request_3344\GIS_Data_Request_3344\Data.gdb\HS2_HSTWO_SafeguardingAndZonedPropertySchemes_Ply"
LocalAuthority = r"C:\Users\ukodb001\Desktop\Tasks\2020\GSSGISK-2039_Create_Constituency_Local_Authority_Boundaries_for_Safeguarding\Output.gdb\Local_AuthoritiesAmended_20200304"
Constituency = r"C:\Users\ukodb001\Desktop\Tasks\2020\GSSGISK-2039_Create_Constituency_Local_Authority_Boundaries_for_Safeguarding\Output.gdb\ConstituenciesAmended_20200304"
AddressPoly = r"C:\Users\ukodb001\Desktop\Tasks\2020\GSSGISK-2236_Finalise_HS2B_2020_Safeguarding_Script\Incoming\SG_Input\Raw.gdb\AddressBasePremium_Polygon"
AddressNonPoly = r"C:\Users\ukodb001\Desktop\Tasks\2020\GSSGISK-2236_Finalise_HS2B_2020_Safeguarding_Script\Incoming\SG_Input\Raw.gdb\AddressBasePremium_NonPolygon"

# Take a copy of Land Ownerships and move to the working folder so that the input data is not changed in anyway
requiredLOP = arcpy.Select_analysis(LandOwnershipParcels, str(Output)+"\Required_LOP")

print "Output Land Ownership Parcel copy complete"

# Select the required zones from the input Safeguarding data
SelectNewZones = arcpy.Select_analysis(NewSafeguardingZones, str(Working)+"\Parcel_ZoneSelectNew", """Zone_Type <> 'SGLim' AND Currency = 'Current' AND HS2_Phase = 'R4'""")
SelectOldZones = arcpy.Select_analysis(OldSafeguardingZones, str(Working)+"\Parcel_ZoneSelectOld", """Zone_Type <> 'SGLim' AND Currency = 'Current' AND HS2_Phase = 'R4'""")

print "Required safeguarding zone selection complete"

# Intersect the Land Ownership Parcels with the Safeguarding Zones
IntersectNewZones = arcpy.Intersect_analysis([requiredLOP,SelectNewZones], str(Working)+"\Parcel_ZoneIntersectNew", "ALL", "", "INPUT")
IntersectOldZones = arcpy.Intersect_analysis([requiredLOP,SelectOldZones], str(Working)+"\Parcel_ZoneIntersectOld", "ALL", "", "INPUT")

print "Required safeguarding zone intersection with working Land Ownership Parcel complete"

# Dissolve the intersected LOP and Safeguarding Zones
DissolveNewZones = arcpy.Dissolve_management(IntersectNewZones, str(Working)+"\Parcel_ZoneDissolveNew", [LOPField,"Zone_Type"], "", "", "")
DissolveOldZones = arcpy.Dissolve_management(IntersectOldZones, str(Working)+"\Parcel_ZoneDissolveOld", [LOPField,"Zone_Type"], "", "", "")

# Intersect Addresses, Local Authorities and Constituencies
intersectPolyAddress = arcpy.Intersect_analysis([requiredLOP,AddressPoly], str(Working)+"\Parcel_LOPABPPolyintersect", "ALL", "", "INPUT")
dissolvePolyAddress = arcpy.Dissolve_management(intersectPolyAddress, str(Working)+"\Parcel_LOPABPPolyDissolve", LOPField, "", "", "")
intersectNonPolyAddress = arcpy.Intersect_analysis([requiredLOP,AddressNonPoly], str(Working)+"\Parcel_LOPABPNonPolyintersect", "ALL", "", "INPUT")
dissolveNonPolyAddress = arcpy.Dissolve_management(intersectNonPolyAddress, str(Working)+"\Parcel_LOPABPNonPolyDissolve", LOPField, "", "", "")
localauthorityintersect = arcpy.Intersect_analysis([requiredLOP,LocalAuthority], str(Working)+"\Parcel_LocalAuthorityIntersect", "ALL", "", "INPUT")
localauthoritydissolve = arcpy.Dissolve_management(localauthorityintersect, str(Working)+"\Parcel_LocalAuthorityDissolve", [LOPField,"lad17nm"], "", "", "")
constituencyintersect = arcpy.Intersect_analysis([requiredLOP,Constituency], str(Working)+"\Parcel_constituencyIntersect", "ALL", "", "INPUT")
constituencydissolve = arcpy.Dissolve_management(constituencyintersect, str(Working)+"\Parcel_constituencyDissolve", [LOPField,"pcon15nm"], "", "", "")

print "Intersect Addresses, Local Authorities and Constituencies complete"

# Add Intersection area fields to dissolved layers
addsurfaceareanew = arcpy.AddField_management(requiredLOP, newsurfaceareafield, FieldType, "",field_alias="Surface Area New")
addsurfaceareaold = arcpy.AddField_management(requiredLOP, oldsurfaceareafield, FieldType, "",field_alias="Surface Area Old")
addsubsurfaceareanew = arcpy.AddField_management(requiredLOP, newsubsurfaceareafield, FieldType, "",field_alias="SubSurface Area New")
addsubsurfaceareaold = arcpy.AddField_management(requiredLOP, oldsubsurfaceareafield, FieldType, "",field_alias="SubSurface Area Old")
addEHPZ1areanew = arcpy.AddField_management(requiredLOP, newEHPZ1areafield, FieldType, "",field_alias="EHPZ1 Area New")
addEHPZ1areaold = arcpy.AddField_management(requiredLOP, oldEHPZ1areafield, FieldType, "",field_alias="EHPZ1 Area Old")
addEHPZ2areanew = arcpy.AddField_management(requiredLOP, newEHPZ2areafield, FieldType, "",field_alias="EHPZ2 Area New")
addEHPZ2areaold = arcpy.AddField_management(requiredLOP, oldEHPZ2areafield, FieldType, "",field_alias="EHPZ2 Area Old")
addEHPZ3areanew = arcpy.AddField_management(requiredLOP, newEHPZ3areafield, FieldType, "",field_alias="EHPZ3 Area New")
addEHPZ3areaold = arcpy.AddField_management(requiredLOP, oldEHPZ3areafield, FieldType, "",field_alias="EHPZ3 Area Old")
addRSZareanew = arcpy.AddField_management(requiredLOP, newRSZareafield, FieldType, "",field_alias="RSZ Area New")
addRSZareaold = arcpy.AddField_management(requiredLOP, oldRSZareafield, FieldType, "",field_alias="RSZ Area Old")
addHOP1areanew = arcpy.AddField_management(requiredLOP, newHOP1areafield, FieldType, "",field_alias="HOP1 Area New")
addHOP1areaold = arcpy.AddField_management(requiredLOP, oldHOP1areafield, FieldType, "",field_alias="HOP1 Area Old")
addHOP2areanew = arcpy.AddField_management(requiredLOP, newHOP2areafield, FieldType, "",field_alias="HOP2 Area New")
addHOP2areaold = arcpy.AddField_management(requiredLOP, oldHOP2areafield, FieldType, "",field_alias="HOP2 Area Old")
addHOP3areanew = arcpy.AddField_management(requiredLOP, newHOP3areafield, FieldType, "",field_alias="HOP3 Area New")
addHOP3areaold = arcpy.AddField_management(requiredLOP, oldHOP3areafield, FieldType, "",field_alias="HOP3 Area Old")
addHOPTotalareafieldnew = arcpy.AddField_management(requiredLOP, newHOPTotalareafield, FieldType, "",field_alias="HOP Total Area New")
addHOPTotalareafieldold = arcpy.AddField_management(requiredLOP, oldHOPTotalareafield, FieldType, "",field_alias="HOP Total Area Old")

# Add Intersection percentage fields to dissolved layers
addsurfacepercentagenew = arcpy.AddField_management(requiredLOP, newsurfacepercentagefield, FieldType, "",field_alias="Surface Percentage New")
addsurfacepercentageold = arcpy.AddField_management(requiredLOP, oldsurfacepercentagefield, FieldType, "",field_alias="Surface Percentage Old")
addsubsurfacepercentagenew = arcpy.AddField_management(requiredLOP, newsubsurfacepercentagefield, FieldType, "",field_alias="SubSurface Percentage New")
addsubsurfacepercentageold = arcpy.AddField_management(requiredLOP, oldsubsurfacepercentagefield, FieldType, "",field_alias="SubSurface Percentage Old")
addEHPZ1percentagenew = arcpy.AddField_management(requiredLOP, newEHPZ1percentagefield, FieldType, "",field_alias="EHPZ1 Percentage New")
addEHPZ1percentageold = arcpy.AddField_management(requiredLOP, oldEHPZ1percentagefield, FieldType, "",field_alias="EHPZ1 Percentage Old")
addEHPZ2percentagenew = arcpy.AddField_management(requiredLOP, newEHPZ2percentagefield, FieldType, "",field_alias="EHPZ2 Percentage New")
addEHPZ2percentageold = arcpy.AddField_management(requiredLOP, oldEHPZ2percentagefield, FieldType, "",field_alias="EHPZ2 Percentage Old")
addEHPZ3percentagenew = arcpy.AddField_management(requiredLOP, newEHPZ3percentagefield, FieldType, "",field_alias="EHPZ3 Percentage New")
addEHPZ3percentageold = arcpy.AddField_management(requiredLOP, oldEHPZ3percentagefield, FieldType, "",field_alias="EHPZ3 Percentage Old")
addRSZpercentagenew = arcpy.AddField_management(requiredLOP, newRSZpercentagefield, FieldType, "",field_alias="RSZ Percentage New")
addRSZpercentageold = arcpy.AddField_management(requiredLOP, oldRSZpercentagefield, FieldType, "",field_alias="RSZ Percentage Old")
addHOP1percentagenew = arcpy.AddField_management(requiredLOP, newHOP1percentagefield, FieldType, "",field_alias="HOP1 Percentage New")
addHOP1percentageold = arcpy.AddField_management(requiredLOP, oldHOP1percentagefield, FieldType, "",field_alias="HOP1 Percentage Old")
addHOP2percentagenew = arcpy.AddField_management(requiredLOP, newHOP2percentagefield, FieldType, "",field_alias="HOP2 Percentage New")
addHOP2percentageold = arcpy.AddField_management(requiredLOP, oldHOP2percentagefield, FieldType, "",field_alias="HOP2 Percentage Old")
addHOP3percentagenew = arcpy.AddField_management(requiredLOP, newHOP3percentagefield, FieldType, "",field_alias="HOP3 Percentage New")
addHOP3percentageold = arcpy.AddField_management(requiredLOP, oldHOP3percentagefield, FieldType, "",field_alias="HOP3 Percentage Old")
addHOPTotalpercentagefieldnew = arcpy.AddField_management(requiredLOP, newHOPTotalpercentagefield, FieldType, "",field_alias="HOP Percentage Area New")
addHOPTotalpercentagefieldold = arcpy.AddField_management(requiredLOP, oldHOPTotalpercentagefield, FieldType, "",field_alias="HOP Percentage Area Old")

# Add Intersection integer fields to dissolved layers
addSGSurIntegernew = arcpy.AddField_management(requiredLOP, newSGSurIntegerfield, intfieldtype, "",field_alias="Surface Integer New")
addSGSurIntegerold = arcpy.AddField_management(requiredLOP, oldSGSurIntegerfield, intfieldtype, "",field_alias="Surface Integer Old")
addSGSubIntegernew = arcpy.AddField_management(requiredLOP, newSGSubIntegerfield , intfieldtype, "",field_alias="SubSurface Integer New")
addSGSubIntegerold = arcpy.AddField_management(requiredLOP, oldSGSubIntegerfield, intfieldtype, "",field_alias="SubSurface Integer Old")
addEHPZ1Integernew = arcpy.AddField_management(requiredLOP, newEHPZ1Integerfield, intfieldtype, "",field_alias="EHPZ1 Integer New")
addEHPZ1Integerold = arcpy.AddField_management(requiredLOP, oldEHPZ1Integerfield, intfieldtype, "",field_alias="EHPZ1 Integer Old")
addEHPZ2Integernew = arcpy.AddField_management(requiredLOP, newEHPZ2Integerfield, intfieldtype, "",field_alias="EHPZ2 Integer New")
addEHPZ2Integerold = arcpy.AddField_management(requiredLOP, oldEHPZ2Integerfield, intfieldtype, "",field_alias="EHPZ2 Integer Old")
addEHPZ3Integernew = arcpy.AddField_management(requiredLOP, newEHPZ3Integerfield, intfieldtype, "",field_alias="EHPZ3 Integer New")
addEHPZ3Integerold = arcpy.AddField_management(requiredLOP, oldEHPZ3Integerfield, intfieldtype, "",field_alias="EHPZ3 Integer Old")
addRSZIntegernew = arcpy.AddField_management(requiredLOP, newRSZIntegerfield, intfieldtype, "",field_alias="RSZ Integer New")
addRSZIntegerold = arcpy.AddField_management(requiredLOP, oldRSZIntegerfield, intfieldtype, "",field_alias="RSZ Integer Old")
addHOP1Integernew = arcpy.AddField_management(requiredLOP, newHOP1Integerfield, intfieldtype, "",field_alias="HOP1 Integer New")
addHOP1Integerold = arcpy.AddField_management(requiredLOP, oldHOP1Integerfield, intfieldtype, "",field_alias="HOP1 Integer Old")
addHOP2Integernew = arcpy.AddField_management(requiredLOP, newHOP2Integerfield, intfieldtype, "",field_alias="HOP2 Integer New")
addHOP2Integerold = arcpy.AddField_management(requiredLOP, oldHOP2Integerfield, intfieldtype, "",field_alias="HOP2 Integer Old")
addHOP3Integernew = arcpy.AddField_management(requiredLOP, newHOP3Integerfield, intfieldtype, "",field_alias="HOP3 Integer New")
addHOP3Integerold = arcpy.AddField_management(requiredLOP, oldHOP3Integerfield, intfieldtype, "",field_alias="HOP3 Integer Old")
addInHOPfieldnew = arcpy.AddField_management(requiredLOP, newInHOPfield, FieldType, "",field_alias="In HOP New")
addInHOPfieldold = arcpy.AddField_management(requiredLOP, oldInHOPfield, FieldType, "",field_alias="In HOP Old")
addnewNoZonefield = arcpy.AddField_management(requiredLOP, NewNoZonefield, FieldType, "",field_alias="No Zone New")
addoldNoZonefield = arcpy.AddField_management(requiredLOP, OldNoZonefield, FieldType, "",field_alias="No Zone Old") 
addcontainsaddress = arcpy.AddField_management(requiredLOP, AddressPresentField, "Text", "",field_alias="Contains Address")
addscenariofield = arcpy.AddField_management(requiredLOP, scenario, "TEXT", "",field_alias="Scenario")
#addscenariofield = arcpy.AddField_management(requiredLOP, scenario, FieldType, "",field_alias="Scenario")
addscenariotextfield = arcpy.AddField_management(requiredLOP, scenariotext, "TEXT", "",field_length = 500, field_alias="Scenario Text")
addgisreviewfield = arcpy.AddField_management(requiredLOP, gisreview, "TEXT", "",field_length = 500, field_alias="GIS Comment")
addexclusionfield = arcpy.AddField_management(requiredLOP, exclusion, "TEXT", "",field_length = 500, field_alias="Exclusion Reason")
addHOPScenariofield = arcpy.AddField_management(requiredLOP, HOPScenario, FieldType, "",field_alias="HOP Scenario")
addHOPScenariotextfield = arcpy.AddField_management(requiredLOP, HOPScenariotext, "TEXT", "",field_length = 500, field_alias="HOP Scenario Text")

lafields = ["OwnershipReferenceNumber","lad17nm"]

# Create a dictionary to hold Ownership Reference Numbers and the Local Authorities in a list grouped by key
ladict = {}
with arcpy.da.SearchCursor(localauthoritydissolve, lafields) as lacursor:
    for larow in lacursor:
        key = larow[0]
        value = larow[1]
        if ladict.has_key(key):
            ladict[key].append(value)       
        else:
            ladict[key] = [value]

# Create a dictionary to count the number of Local Authority values each Ownership Reference Numbers key holds within its list
lacount = {}
for key, values in ladict.items():
        lacount[key] = len(values)

# Create a dictionary to group the two dictionaries above using tuples 
lacombined = {}
for key in ladict.iterkeys():
    lacombined[key] = list(lacombined[key] for lacombined in [ladict, lacount])

# Identify the maximum number of Local Authority Intersections 
maximumlavalue = max(lacount.iteritems(), key=operator.itemgetter(1))[1]
# Start a loop to add a field for each intersection, then calculate each field added 
for i in range(maximumlavalue):
    addlafields = arcpy.AddField_management(requiredLOP, "LocalAuthority_"+str(i+1), "TEXT", "",field_alias="Local Authority "+str(i+1))
    # Create a conditional dictionary whos values are equal to that of i+1
    ladictcalc = {key:val for key, val in lacombined.items() if lacombined[key][-1] >= i+1}
    # Check for a Local Authority field each time iteration runs
    lacheckfields = arcpy.ListFields(requiredLOP,"LocalAuthority_*")
    lacheckerfields = [LOPField]
    for field in lacheckfields:
        lacheckerfields.append(field.name)
    # Use an update cursor to calculate each row as it is added based on the values of i
    with arcpy.da.UpdateCursor(requiredLOP, lacheckerfields) as updateRows:  
        for updateRow in updateRows:
            # store the Join value of the row being updated in a keyValue variable  
            keyValue = updateRow[0]  
            # verify that the keyValue is in the Dictionary  
            if keyValue in ladictcalc:  
                # transfer the value stored under the keyValue from the dictionary to the updated field.  
                updateRow[i+1] = ladictcalc[keyValue][0][i]
            updateRows.updateRow(updateRow)

print "Local Authorities Populated"

cfields = ["OwnershipReferenceNumber","pcon15nm"]

# Create a dictionary to hold Ownership Reference Numbers and the Constituencies in a list grouped by key
cdict = {}
with arcpy.da.SearchCursor(constituencydissolve, cfields) as ccursor:
    for crow in ccursor:
        key = crow[0]
        value = crow[1]
        if cdict.has_key(key):
            cdict[key].append(value)       
        else:
            cdict[key] = [value]

# Create a dictionary to count the number of Constituency values each Ownership Reference Numbers key holds within its list
ccount = {}
for key, values in cdict.items():
        ccount[key] = len(values)

# Create a dictionary to group the two dictionaries above using tuples 
ccombined = {}
for key in cdict.iterkeys():
    ccombined[key] = list(ccombined[key] for ccombined in [cdict, ccount])

# Identify the maximum number of Constituency Intersections 
maximumcvalue = max(ccount.iteritems(), key=operator.itemgetter(1))[1]
# Start a loop to add a field for each intersection, then calcucte each field added 
for i in range(maximumcvalue):
    addcfields = arcpy.AddField_management(requiredLOP, "Constituency_"+str(i+1), "TEXT", "",field_alias="Constituency "+str(i+1))
    # Create a conditional dictionary whos values are equal to that of i+1
    cdictcalc = {key:val for key, val in ccombined.items() if ccombined[key][-1] >= i+1}
    # Check for a Constituency field each time iteration runs
    ccheckfields = arcpy.ListFields(requiredLOP,"Constituency_*")
    ccheckerfields = [LOPField]
    for field in ccheckfields:
        ccheckerfields.append(field.name)
    # Use an update cursor to calcucte each row as it is added based on the values of i
    with arcpy.da.UpdateCursor(requiredLOP, ccheckerfields) as updateRows:  
        for updateRow in updateRows:
            # store the Join value of the row being updated in a keyValue variable  
            keyValue = updateRow[0]  
            # verify that the keyValue is in the Dictionary  
            if keyValue in cdictcalc:  
                # transfer the value stored under the keyValue from the dictionary to the updated field.  
                updateRow[i+1] = cdictcalc[keyValue][0][i]
            updateRows.updateRow(updateRow)

print "Constituency Populated"

# List fields in inputs
newzonefields = [f.name for f in arcpy.ListFields(DissolveNewZones)]
oldzonefields = [f.name for f in arcpy.ListFields(DissolveOldZones)]
polyaddressfields = [f.name for f in arcpy.ListFields(dissolvePolyAddress)]
nonpolyaddressfields = [f.name for f in arcpy.ListFields(dissolveNonPolyAddress)]
localauthorityfields = [f.name for f in arcpy.ListFields(localauthoritydissolve)]
constituencyfields = [f.name for f in arcpy.ListFields(constituencydissolve)]
requiredLOPfields = [f.name for f in arcpy.ListFields(requiredLOP)]

# Set Null values within the Required_LOP feature class to zero
with arcpy.da.UpdateCursor(requiredLOP, requiredLOPfields) as setzerocursor:
    for rowzero in setzerocursor:
        updated = False
        for i, c in enumerate(requiredLOPfields):
            if rowzero[i] == None:
                rowzero[i] = 0
                updated = True
        if updated == True:
            setzerocursor.updateRow(rowzero)

# Calculate Intersection Area, Percentage and Integer fields
# Create dictionaries to hold values
newsurvalueDict = {}
oldsurvalueDict = {}
newsubvalueDict = {}
oldsubvalueDict = {}
newEHPZ1valueDict = {}
oldEHPZ1valueDict = {}
newEHPZ2valueDict = {}
oldEHPZ2valueDict = {}
newEHPZ3valueDict = {}
oldEHPZ3valueDict = {}
newRSZvalueDict = {}
oldRSZvalueDict = {}
newHOP1valueDict = {}
oldHOP1valueDict = {}
newHOP2valueDict = {}
oldHOP2valueDict = {}
newHOP3valueDict = {}
oldHOP3valueDict = {}
polyaddressfieldsvalueDict = {}
nonpolyaddressfieldsvalueDict = {}

# Create a search cursor on the NEW dissolved Parcel and Zone intersection to load the NEW dictionaries above with ownership reference number as the key
# and the corresponding Shape_Area for each ORN as the value, based on each Safeguarding Zone type
with arcpy.da.SearchCursor(DissolveNewZones, newzonefields) as scursor:
    for srow in scursor:
        key = srow[2]
        value = srow[5]
        if srow[3] == "SGSur":
            newsurvalueDict[key] = value
        if srow[3] == "SGSub":
            newsubvalueDict[key] = value
        if srow[3] == "EHPZ1":
            newEHPZ1valueDict[key] = value
        if srow[3] == "EHPZ2":
            newEHPZ2valueDict[key] = value
        if srow[3] == "EHPZ3":
            newEHPZ3valueDict[key] = value
        if srow[3] == "RSZ":
            newRSZvalueDict[key] = value
        if srow[3] == "HOP1":
            newHOP1valueDict[key] = value
        if srow[3] == "HOP2":
            newHOP2valueDict[key] = value
        if srow[3] == "HOP3":
            newHOP3valueDict[key] = value

# Create a search cursor on the OLD dissolved Parcel and Zone intersection to load the OLD dictionaries above with ownership reference number as the key
# and the corresponding Shape_Area for each ORN as the value, based on each Safeguarding Zone type
with arcpy.da.SearchCursor(DissolveOldZones, oldzonefields) as scursor:
    for srow in scursor:
        key = srow[2]
        value = srow[5]
        if srow[3] == "SGSur":
            oldsurvalueDict[key] = value
        if srow[3] == "SGSub":
            oldsubvalueDict[key] = value
        if srow[3] == "EHPZ1":
            oldEHPZ1valueDict[key] = value
        if srow[3] == "EHPZ2":
            oldEHPZ2valueDict[key] = value
        if srow[3] == "EHPZ3":
            oldEHPZ3valueDict[key] = value
        if srow[3] == "RSZ":
            oldRSZvalueDict[key] = value
        if srow[3] == "HOP1":
            oldHOP1valueDict[key] = value
        if srow[3] == "HOP2":
            oldHOP2valueDict[key] = value
        if srow[3] == "HOP3":
            oldHOP3valueDict[key] = value

# Create a search cursor on the POLY dissolved intersection with Required_LOP to load the polyaddressfieldsvalueDict dictionary above with ownership reference number as the key
with arcpy.da.SearchCursor(dissolvePolyAddress, polyaddressfields) as scursor:
    for srow in scursor:
        key = srow[2]
        polyaddressfieldsvalueDict[key] = value

# Create a search cursor on the NON-POLY dissolved intersection with Required_LOP to load the polyaddressfieldsvalueDict dictionary above with ownership reference number as the key
with arcpy.da.SearchCursor(dissolveNonPolyAddress, nonpolyaddressfields) as scursor:
    for srow in scursor:
        key = srow[2]
        nonpolyaddressfieldsvalueDict[key] = value

# Update the fields within the Required_LOP feature class with the Shape_Area values within the dictionaries above and calculate Percenatage and Integer fields based on these values
with arcpy.da.UpdateCursor(requiredLOP, requiredLOPfields) as updateRows:  
    for updateRow in updateRows:  
        # store the Join value of the row being updated in a keyValue variable  
        keyValue = updateRow[2]
        # verify that the keyValue is in the Dictionary  
        if keyValue in newsurvalueDict:
            # transfer the value stored under the keyValue from the newsurvalueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW Surface Safeguarding  
            updateRow[9] = newsurvalueDict[keyValue]
            updateRow[29] = updateRow[9] / updateRow[8] * 100
            updateRow[49] = 1 if updateRow[9] >= 1 else updateRow[49]
        # verify that the keyValue is in the Dictionary  
        if keyValue in oldsurvalueDict:
            # transfer the value stored under the keyValue from the newsurvalueDict dictionary to the updated field, then calculate the Percentage and Integer fields for OLD Surface Safeguarding  
            updateRow[10] = oldsurvalueDict[keyValue]
            updateRow[30] = updateRow[10] / updateRow[8] * 100
            updateRow[50] = 1 if updateRow[10] >= 1 else updateRow[50]
        # verify that the keyValue is in the Dictionary  
        if keyValue in newsubvalueDict:
            # transfer the value stored under the keyValue from the newsubvalueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW Subsurface Safeguarding  
            updateRow[11] = newsubvalueDict[keyValue]
            updateRow[31] = updateRow[11] / updateRow[8] * 100
            updateRow[51] = 1 if updateRow[11] >= 1 else updateRow[51]
        # verify that the keyValue is in the Dictionary  
        if keyValue in oldsubvalueDict:
            # transfer the value stored under the keyValue from the newsurvalueDict dictionary to the updated field, then calculate the Percentage and Integer fields for OLD Subsurface Safeguarding  
            updateRow[12] = oldsubvalueDict[keyValue]
            updateRow[32] = updateRow[12] / updateRow[8] * 100
            updateRow[52] = 1 if updateRow[12] >= 1 else updateRow[52]
        # verify that the keyValue is in the Dictionary  
        if keyValue in newEHPZ1valueDict:
            # transfer the value stored under the keyValue from the newEHPZ1valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW EHPZ1  
            updateRow[13] = newEHPZ1valueDict[keyValue]
            updateRow[33] = updateRow[13] / updateRow[8] * 100
            updateRow[53] = 1 if updateRow[13] >= 1 else updateRow[53]
        # verify that the keyValue is in the Dictionary  
        if keyValue in oldEHPZ1valueDict:
            # transfer the value stored under the keyValue from the newsurvalueDict dictionary to the updated field, then calculate the Percentage and Integer fields for OLD EHPZ1  
            updateRow[14] = oldEHPZ1valueDict[keyValue]
            updateRow[34] = updateRow[14] / updateRow[8] * 100
            updateRow[54] = 1 if updateRow[14] >= 1 else updateRow[54]
        # verify that the keyValue is in the Dictionary  
        if keyValue in newEHPZ2valueDict:
            # transfer the value stored under the keyValue from the newEHPZ2valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW EHPZ2  
            updateRow[15] = newEHPZ2valueDict[keyValue]
            updateRow[35] = updateRow[15] / updateRow[8] * 100
            updateRow[55] = 1 if updateRow[15] >= 1 else updateRow[55]
        # verify that the keyValue is in the Dictionary  
        if keyValue in oldEHPZ2valueDict:
            # transfer the value stored under the keyValue from the newsurvalueDict dictionary to the updated field, then calculate the Percentage and Integer fields for OLD EHPZ2   
            updateRow[16] = oldEHPZ2valueDict[keyValue]
            updateRow[36] = updateRow[16] / updateRow[8] * 100
            updateRow[56] = 1 if updateRow[16] >= 1 else updateRow[56]
        # verify that the keyValue is in the Dictionary  
        if keyValue in newEHPZ3valueDict:
            # transfer the value stored under the keyValue from the newEHPZ2valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW EHPZ2  
            updateRow[17] = newEHPZ3valueDict[keyValue]
            updateRow[37] = updateRow[17] / updateRow[8] * 100
            updateRow[57] = 1 if updateRow[17] >= 1 else updateRow[57]
        # verify that the keyValue is in the Dictionary  
        if keyValue in oldEHPZ3valueDict:
            # transfer the value stored under the keyValue from the newsurvalueDict dictionary to the updated field, then calculate the Percentage and Integer fields for OLD EHPZ2   
            updateRow[18] = oldEHPZ3valueDict[keyValue]
            updateRow[38] = updateRow[18] / updateRow[8] * 100
            updateRow[58] = 1 if updateRow[18] >= 1 else updateRow[58]
        # verify that the keyValue is in the Dictionary  
        if keyValue in newRSZvalueDict:
            # transfer the value stored under the keyValue from the newRSZvalueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW RSZ  
            updateRow[19] = newRSZvalueDict[keyValue]
            updateRow[39] = updateRow[19] / updateRow[8] * 100
            updateRow[59] = 1 if updateRow[19] >= 1 else updateRow[59]
        # verify that the keyValue is in the Dictionary  
        if keyValue in oldRSZvalueDict:
            # transfer the value stored under the keyValue from the newRSZvalueDict dictionary to the updated field, then calculate the Percentage and Integer fields for OLD RSZ  
            updateRow[20] = oldRSZvalueDict[keyValue]
            updateRow[40] = updateRow[20] / updateRow[8] * 100
            updateRow[60] = 1 if updateRow[20] >= 1 else updateRow[60]            
        # verify that the keyValue is in the Dictionary  
        if keyValue in newHOP1valueDict:
            # transfer the value stored under the keyValue from the newHOP1valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW HOP1  
            updateRow[21] = newHOP1valueDict[keyValue]
            updateRow[41] = updateRow[21] / updateRow[8] * 100
            updateRow[61] = 1 if updateRow[21] >= 1 else updateRow[61]
        # verify that the keyValue is in the Dictionary  
        if keyValue in oldHOP1valueDict:
            # transfer the value stored under the keyValue from the newHOP1valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for OLD HOP1  
            updateRow[22] = oldHOP1valueDict[keyValue]
            updateRow[42] = updateRow[22] / updateRow[8] * 100
            updateRow[62] = 1 if updateRow[22] >= 1 else updateRow[62]
        # verify that the keyValue is in the Dictionary  
        if keyValue in newHOP2valueDict:
            # transfer the value stored under the keyValue from the newHOP2valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW HOP2   
            updateRow[23] = newHOP2valueDict[keyValue]
            updateRow[43] = updateRow[23] / updateRow[8] * 100
            updateRow[63] = 1 if updateRow[23] >= 1 else updateRow[63]
        # verify that the keyValue is in the Dictionary  
        if keyValue in oldHOP2valueDict:
            # transfer the value stored under the keyValue from the newHOP2valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for OLD HOP2 
            updateRow[24] = oldHOP2valueDict[keyValue]
            updateRow[44] = updateRow[24] / updateRow[8] * 100
            updateRow[64] = 1 if updateRow[24] >= 1 else updateRow[64]
        # verify that the keyValue is in the Dictionary  
        if keyValue in newHOP3valueDict:
            # transfer the value stored under the keyValue from the newHOP3valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW HOP3  
            updateRow[25] = newHOP3valueDict[keyValue]
            updateRow[45] = updateRow[25] / updateRow[8] * 100
            updateRow[65] = 1 if updateRow[25] >= 1 else updateRow[65]
        # verify that the keyValue is in the Dictionary  
        if keyValue in oldHOP3valueDict:
            # transfer the value stored under the keyValue from the newHOP3valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for OLD HOP3  
            updateRow[26] = oldHOP3valueDict[keyValue]
            updateRow[46] = updateRow[26] / updateRow[8] * 100
            updateRow[66] = 1 if updateRow[26] >= 1 else updateRow[66]
        # Calculate HOPTotalArea_NEW
        if updateRow[21] >= 1 or updateRow[23] >= 1 or updateRow[25] >= 1:
            updateRow[27] = updateRow[21] + updateRow[23] + updateRow[25]
        # Calculate HOPTotalArea_OLD
        if updateRow[22] >= 1 or updateRow[24] >= 1 or updateRow[26] >= 1:
            updateRow[28] = updateRow[22] + updateRow[24] + updateRow[26]
        # Calculate HOPTotalPercentage_NEW
        if updateRow[27] / updateRow[8] * 100 > 0:
            updateRow[47] = updateRow[27] / updateRow[8] * 100
        # Calculate HOPTotalPercentage_OLD
        if updateRow[28] / updateRow[8] * 100 > 0:
            updateRow[48] = updateRow[28] / updateRow[8] * 100
        # Calculate In_HOP_NEW
        if updateRow[21] >= 1 or updateRow[23] >= 1 or updateRow[25] >= 1:
            updateRow[67] = 1
        # Calculate In_HOP_OLD
        if updateRow[22] >= 1 or updateRow[24] >= 1 or updateRow[26] >= 1:
            updateRow[68] = 1
        # Calculate No_Zone_NEW
        if updateRow[9] <= 1 and updateRow[11] <= 1 and updateRow[13] <= 1 and updateRow[15] <= 1 and updateRow[17] <= 1 and updateRow[19] <= 1 and updateRow[21] <= 1 and updateRow[23] <= 1 and updateRow[25] <= 1:
            updateRow[69] = 1
        # Calculate No_Zone_OLD
        if updateRow[10] <= 1 and updateRow[12] <= 1 and updateRow[14] <= 1 and updateRow[16] <= 1 and updateRow[18] <= 1 and updateRow[20] <= 1 and updateRow[22] <= 1 and updateRow[24] <= 1 and updateRow[26] <= 1:
            updateRow[70] = 1
        # verify that the keyValue is in the Dictionary  
        if keyValue in polyaddressfieldsvalueDict:
            # transfer the value stored under the keyValue from the newHOP3valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW HOP3  
            updateRow[71] = "Yes"
        if keyValue in nonpolyaddressfieldsvalueDict:
            # transfer the value stored under the keyValue from the newHOP3valueDict dictionary to the updated field, then calculate the Percentage and Integer fields for NEW HOP3  
            updateRow[71] = "Yes"
        updateRows.updateRow(updateRow)

del newsurvalueDict,newsubvalueDict,newEHPZ1valueDict,newEHPZ2valueDict,newEHPZ3valueDict,newRSZvalueDict,newHOP1valueDict,newHOP2valueDict,newHOP3valueDict,oldsurvalueDict,oldsubvalueDict,oldEHPZ1valueDict,oldEHPZ2valueDict,oldEHPZ3valueDict,oldRSZvalueDict,oldHOP1valueDict,oldHOP2valueDict,oldHOP3valueDict

print "Intersection Area, Percentage and Integer field calculations complete"

#Capture end time of script
print 'Safeguarding finished in: %s\n\n' % (datetime.now() - start)
