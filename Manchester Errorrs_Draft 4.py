#-------------------------------------------------------------------------------
# Name:        Hs2a (C863), Hs2B Lot 1 (2C864), & Hs2B Lot 3 (C866)
#              outstanding amends email report
# Purpose:     Better Monitor Hs2 workload and data management
#
# Author:      Kane Russell
#
# Created:     24/06/2019
# Copyright:   (c) UKKXR602 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
import shutil
import csv
import win32com.client as win32
import datetime

#Date
now = datetime.datetime.now()
Date = now.strftime("%Y%m%d%H%M")

#Create work space
desktopPath = os.environ.get( "USERPROFILE" ) + "\\Desktop"
os.makedirs(desktopPath + "\\Hs2_Scheme_Review_" + str(Date))
TempFolder = desktopPath + "\\Hs2_Scheme_Review_" + str(Date)

#Choose Work Database To Run QC Check
SDE_Geodatabase = r"Database Connections\HS2-Phase2A-Manchester-GSS.sde"
WorkFolder = TempFolder

#Delete Previous GDB from shared drive
WorkFolder2 = r"\\cormplbrbs1.corp.pbwan.net\Shared\LandAspects\GSS\Admin\Kane\Test"
arcpy.env.workspace = WorkFolder2
GDB = arcpy.ListWorkspaces("","FileGDB")

for gd in GDB:
    arcpy.Delete_management(gd)

print('Shared Folder cleared')
#Set Work Folder
print("Creating Local QC Copy of Phase 2A")
GDB = "QC_Work_GDD_Manchester_2a"
WorkGDD = WorkFolder + "\\" + GDB + ".gdb"
arcpy.env.workspace = SDE_Geodatabase
arcpy.CreateFileGDB_management(WorkFolder,GDB)

#set Calculator Variables
fieldName = "Dup"
expression = 'isDuplicateIndex( !LicenceID! )'
expression2 = 'isDuplicateIndex( !OwnershipReferenceNumber! )'
expression3 = 'isDuplicateIndex( !SHAPE_Area! )'
codeblock = """
UniqueDict = {}
def isDuplicateIndex(inValue):
    UniqueDict.setdefault(inValue,0)
    UniqueDict[inValue] += 1
    return UniqueDict[inValue]"""

#List feature classes in dataset
fc_List = arcpy.ListFeatureClasses("","","STATUTORY_PROCESSES")
QC_Features = ['LandOwnershipParcels','AccessLicences']

#Copy Licence and Parcel Feature Class to run QC on
for fc in QC_Features:
    if fc in QC_Features:
        arcpy.CopyFeatures_management(
            fc, os.path.join(WorkGDD,
                         os.path.basename(fc).split('\\')[0]))

#Re-set GDB to Work Folder
arcpy.env.workspace = WorkGDD
GDD_FC_List = arcpy.ListFeatureClasses()

#seperate licence layer into seperate licence types (NL, L, & G)
print("Copying Features To Desktop")
arcpy.FeatureClassToFeatureClass_conversion("AccessLicences",WorkGDD,"GI_Licences",
            "LicenceID LIKE 'G%'")
arcpy.FeatureClassToFeatureClass_conversion("AccessLicences",WorkGDD,"NL_Licences",
            "LicenceID LIKE'NL%'")
arcpy.FeatureClassToFeatureClass_conversion("AccessLicences",WorkGDD,"EAA_Licences",
            "LicenceID LIKE'L%'")
arcpy.Delete_management(WorkGDD + '\\' + 'AccessLicences')

fcs_revised = arcpy.ListFeatureClasses()

#Check for duplicates
print("Checking for duplicates")
LicenceList = ['GI_Licences','NL_Licences','EAA_Licences']
Ownership = ['LandOwnershipParcels']
#Run Initial QC Checks
for fc1 in fcs_revised:
    if fc1 in LicenceList:
        arcpy.Statistics_analysis(fc1,fc1 + '_Duplicate',"LicenceID COUNT","LicenceID")
    else:
        if fc1 in Ownership:
            arcpy.Statistics_analysis(fc1, fc1 + '_Duplicate',"OwnershipReferenceNumber COUNT",
                "OwnershipReferenceNumber")

print("Running Intersect and Multipart Checks")
for fcs in fcs_revised:
    arcpy.Intersect_analysis(fcs,fcs + "_Int","ALL","","INPUT")
    arcpy.MultipartToSinglepart_management(fcs,fcs + "_MultiParts")

#Check for overlapping features and if present export to GDD
OverlapList = arcpy.ListFeatureClasses()

for fcs2 in OverlapList:
    if "_Int" in fcs2:
        arcpy.MakeFeatureLayer_management(fcs2)
        if arcpy.management.GetCount(fcs2)[0] == "0":
            arcpy.Delete_management(fcs2)
            print("No Overlaps Present in " + fcs2)
        else:
            arcpy.AddField_management(fcs2,"Dup","SHORT")
            arcpy.CalculateField_management(fcs2,fieldName,expression3,
                "PYTHON_9.3", codeblock)
            with arcpy.da.UpdateCursor(fcs2,'Dup') as cursor:
                for row in cursor:
                    if row[0] == 1:
                        cursor.deleteRow()
            print("Overlaps Present in " + fcs2)

#Check for multipart features in Land Parcel Data
Parcel_Count = arcpy.GetCount_management('LandOwnershipParcels')
Pcount = int(Parcel_Count.getOutput(0))
print(str(Pcount) + ' Parcels in Original LOP Layer')
Parcel_Multi_Count = arcpy.GetCount_management('LandOwnershipParcels_MultiParts')
MPcount = int(Parcel_Multi_Count.getOutput(0))
print(str(MPcount) + ' Parcels in Exploded LOP Layer')

if Pcount != MPcount:
    arcpy.AddField_management('LandOwnershipParcels_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('LandOwnershipParcels_MultiParts',
        fieldName,expression2,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('LandOwnershipParcels_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("LandOwnershipParcels","OwnershipReferenceNumber",
                    "LandOwnershipParcels_MultiParts","OwnershipReferenceNumber","Dup")
    with arcpy.da.UpdateCursor('LandOwnershipParcels','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('LandOwnershipParcels_MultiParts')
    print("Multipart Feature Present in LOP Layer")
else:
    if Pcount == MPcount:
        arcpy.Delete_management('LandOwnershipParcels_MultiParts')
        arcpy.Delete_management('LandOwnershipParcels')
        print('No Multipart Features in LOP Layer')

#Check for multipart features in Access Licence Data
Licence_count = arcpy.GetCount_management('EAA_Licences')
Lcount = int(Licence_count.getOutput(0))
print(str(Lcount) + ' Parcels in EAA Layer')
Licence_Multi_Count = arcpy.GetCount_management('EAA_Licences_MultiParts')
MLcount = int(Licence_Multi_Count.getOutput(0))
print(str(MLcount) + ' Parcels in Exploded EAA Layer')

if Lcount != MLcount:
    arcpy.AddField_management('EAA_Licences_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('EAA_Licences_MultiParts',
        fieldName,expression,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('EAA_Licences_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("EAA_Licences","LicenceID",
                    "EAA_Licences_MultiParts","LicenceID",'Dup')
    with arcpy.da.UpdateCursor('EAA_Licences','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('EAA_Licences')
    print("Multipart Feature Present in Access Licence Layer")
else:
    if Lcount == MLcount:
        arcpy.Delete_management('EAA_Licences_MultiParts')
        arcpy.Delete_management('EAA_Licences')
        print('No Multipart Features in Access Licence Layer')

#Check for multipart features in Ground Licence Data
GLicence_Count = arcpy.GetCount_management('GI_Licences')
Gcount = int(GLicence_Count.getOutput(0))
print(str(Gcount) + ' Parcels in GI Layer')
GLicence_Multi_count = arcpy.GetCount_management('GI_Licences_MultiParts')
MGcount = int(GLicence_Multi_count.getOutput(0))
print(str(MGcount) + ' Parcels in Exploded GI Layer')

if Gcount != MGcount:
    arcpy.AddField_management('GI_Licences_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('GI_Licences_MultiParts',
        fieldName,expression,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('GI_Licences_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("GI_Licences","LicenceID",
                    "GI_Licences_MultiParts","LicenceID","Dup")
    with arcpy.da.UpdateCursor('GI_Licences','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('GI_Licences')
    print("Multipart Feature Present in GI Layer")
else:
    if Gcount == MGcount:
        arcpy.Delete_management('GI_Licences_MultiParts')
        arcpy.Delete_management('GI_Licences')
        print('No Multipart Features in GI Licence')

#Check for multipart features in Noise Licence Data
NLicence_Count = arcpy.GetCount_management('NL_Licences')
NLCount = int(NLicence_Count.getOutput(0))
print(str(NLCount) + ' Parcels in NL Layer')
MNLicence_Count = arcpy.GetCount_management('NL_Licences_MultiParts')
MNL_Count = int(MNLicence_Count.getOutput(0))
print(str(MNL_Count) + ' Parcels in Exploded in NL Layer')

if NLCount != MNL_Count:
    arcpy.AddField_management('NL_Licences_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('NL_Licences_MultiParts',
        fieldName,expression,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('NL_Licences_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("NL_Licences","LicenceID",
                    "NL_Licences_MultiParts","LicenceID","Dup")
    with arcpy.da.UpdateCursor('NL_Licences','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('NL_Licences')
    print("Multipart Feature Present in NL Layer")
else:
    if NLCount == MNL_Count:
        arcpy.Delete_management('NL_Licences_MultiParts')
        arcpy.Delete_management('NL_Licences')
        print('No Multipart Features in NL Licence')

#Find out if overlapping or multipart features are present in each feature class
#then get status and export in CSV report
print("Producing QC Report")

duplicatelist = ['NL_Licences_Duplicate'
                ,'GI_Licences_Duplicate','EAA_Licences_Duplicate']


with arcpy.da.UpdateCursor('LandOwnershipParcels_Duplicate','COUNT_OwnershipReferenceNumber') as cursor:
    for row in cursor:
        if row[0] == 1:
                cursor.deleteRow()
for sum in duplicatelist:
    with arcpy.da.UpdateCursor(sum,'COUNT_LicenceID') as cursor:
        for row in cursor:
            if row[0] == 1:
                cursor.deleteRow()

duplicatelist2 = ['NL_Licences_Duplicate','LandOwnershipParcels_Duplicate',
                'GI_Licences_Duplicate','EAA_Licences_Duplicate']

for duplist2 in duplicatelist2:
    count = arcpy.GetCount_management(duplist2)
    print('Duplicates in ' + str(duplist2) + " " + str(count))
    if arcpy.management.GetCount(duplist2)[0] == "0":
        arcpy.Delete_management(duplist2)

fcs = arcpy.ListFeatureClasses()
QC_table = arcpy.ListTables()

if 'LandOwnershipParcels_MultiParts' in fcs:
    LOP_Multi = arcpy.GetCount_management('LandOwnershipParcels_MultiParts')
else:
    LOP_Multi = 'No'
if 'NL_Licences_MultiParts' in fcs:
    NL_MultiPart = arcpy.GetCount_management('NL_Licences_MultiParts')
else:
    NL_MultiPart = "No"
if 'GI_Licence_MultiParts' in fcs:
    GI_MultiPart = arcpy.GetCount_management('GI_Licence_MultiParts')
else:
    GI_MultiPart = "No"
if 'EAA_Licences_MultiParts' in fcs:
    Access_MultiPart = arcpy.GetCount_management('EAA_Licences_MultiParts')
else:
    Access_MultiPart = "No"
if 'LandOwnershipParcels_Int' in fcs:
    LOP_Overlap = arcpy.GetCount_management('LandOwnershipParcels_Int')
else:
    LOP_Overlap = "No"
if 'EAA_Licences_Int' in fcs:
    Access_Overlap = arcpy.GetCount_management('EAA_Licences_Int')
else:
    Access_Overlap = "No"
if 'GI_Licences_Int' in fcs:
    GI_Overlap = arcpy.GetCount_management('GI_Licences_Int')
else:
    GI_Overlap = "No"
if 'NL_Licences_Int' in fcs:
    NL_Overlap = arcpy.GetCount_management('NL_Licences_Int')
else:
    NL_Overlap = "No"
if 'LandOwnershipParcels_Duplicate' in QC_table:
    LOP_Dup = "Yes"
else:
    LOP_Dup = "No"
if 'NL_Licences_Duplicate' in QC_table:
    NL_Dup = "Yes"
else:
    NL_Dup = "No"
if 'GI_Licences_Duplicate' in QC_table:
    GI_Dup = "Yes"
else:
    GI_Dup = "No"
if 'EAA_Licences_Duplicate' in QC_table:
    EAA_Dup = "Yes"
else:
    EAA_Dup = "No"

csv_output = WorkFolder + "\\" + "QC_Results_2a.csv"

with open(csv_output,'wb') as openCSV:
    a = csv.writer(openCSV)
    message = [['Feature','Overlaps', 'MultiPart','Duplicates']]
    a.writerows(message)
    message = [['Land Parcels', LOP_Overlap, LOP_Multi,LOP_Dup]]
    a.writerows(message)
    message = [['Access Licences', Access_Overlap, Access_MultiPart,EAA_Dup]]
    a.writerows(message)
    message = [['Noise Licences', NL_Overlap, NL_MultiPart,NL_Dup]]
    a.writerows(message)
    message = [['Ground Investigation Licences', GI_Overlap, GI_MultiPart, GI_Dup]]
    a.writerows(message)

#Choose Work Database To Run QC Check
SDE_Geodatabase = r"Database Connections\HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde"

#Set Work Folder
print("Creating Local QC Copy of Phase 2B Lot 1")
GDB = "QC_Work_GDD_Manchester"
WorkGDD = WorkFolder + "\\" + GDB + ".gdb"
arcpy.env.workspace = SDE_Geodatabase
arcpy.CreateFileGDB_management(WorkFolder,GDB)

#set Calculator Variables
fieldName = "Dup"
expression = 'isDuplicateIndex( !LicenceID! )'
expression2 = 'isDuplicateIndex( !OwnershipReferenceNumber! )'
expression3 = 'isDuplicateIndex( !SHAPE_Area! )'
codeblock = """
UniqueDict = {}
def isDuplicateIndex(inValue):
    UniqueDict.setdefault(inValue,0)
    UniqueDict[inValue] += 1
    return UniqueDict[inValue]"""

#List feature classes in dataset
fc_List = arcpy.ListFeatureClasses("","","STATUTORY_PROCESSES")
QC_Features = ['LandOwnershipParcels','AccessLicences']

#Copy Licence and Parcel Feature Class to run QC on
for fc in QC_Features:
    if fc in QC_Features:
        arcpy.CopyFeatures_management(
            fc, os.path.join(WorkGDD,
                         os.path.basename(fc).split('\\')[0]))

#Re-set GDB to Work Folder
arcpy.env.workspace = WorkGDD
GDD_FC_List = arcpy.ListFeatureClasses()

#seperate licence layer into seperate licence types (NL, L, & G)
print("Copying Features To Desktop")
arcpy.FeatureClassToFeatureClass_conversion("AccessLicences",WorkGDD,"GI_Licences",
            "LicenceID LIKE 'G%'")
arcpy.FeatureClassToFeatureClass_conversion("AccessLicences",WorkGDD,"NL_Licences",
            "LicenceID LIKE'NL%'")
arcpy.FeatureClassToFeatureClass_conversion("AccessLicences",WorkGDD,"EAA_Licences",
            "LicenceID LIKE'L%'")
arcpy.Delete_management(WorkGDD + '\\' + 'AccessLicences')

fcs_revised = arcpy.ListFeatureClasses()

#Check for duplicates
print("Checking for duplicates")
LicenceList = ['GI_Licences','NL_Licences','EAA_Licences']
Ownership = ['LandOwnershipParcels']
#Run Initial QC Checks
for fc1 in fcs_revised:
    if fc1 in LicenceList:
        arcpy.Statistics_analysis(fc1,fc1 + '_Duplicate',"LicenceID COUNT","LicenceID")
    else:
        if fc1 in Ownership:
            arcpy.Statistics_analysis(fc1, fc1 + '_Duplicate',"OwnershipReferenceNumber COUNT",
                "OwnershipReferenceNumber")

print("Running Intersect and Multipart Checks")
for fcs in fcs_revised:
    arcpy.Intersect_analysis(fcs,fcs + "_Int","ALL","","INPUT")
    arcpy.MultipartToSinglepart_management(fcs,fcs + "_MultiParts")

#Check for overlapping features and if present export to GDD
OverlapList = arcpy.ListFeatureClasses()

for fcs2 in OverlapList:
    if "_Int" in fcs2:
        arcpy.MakeFeatureLayer_management(fcs2)
        if arcpy.management.GetCount(fcs2)[0] == "0":
            arcpy.Delete_management(fcs2)
            print("No Overlaps Present in " + fcs2)
        else:
            arcpy.AddField_management(fcs2,"Dup","SHORT")
            arcpy.CalculateField_management(fcs2,fieldName,expression3,
                "PYTHON_9.3", codeblock)
            with arcpy.da.UpdateCursor(fcs2,'Dup') as cursor:
                for row in cursor:
                    if row[0] == 1:
                        cursor.deleteRow()
            print("Overlaps Present in " + fcs2)

#Check for multipart features in Land Parcel Data
Parcel_Count = arcpy.GetCount_management('LandOwnershipParcels')
Pcount = int(Parcel_Count.getOutput(0))
print(str(Pcount) + ' Parcels in Original LOP Layer')
Parcel_Multi_Count = arcpy.GetCount_management('LandOwnershipParcels_MultiParts')
MPcount = int(Parcel_Multi_Count.getOutput(0))
print(str(MPcount) + ' Parcels in Exploded LOP Layer')

if Pcount != MPcount:
    arcpy.AddField_management('LandOwnershipParcels_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('LandOwnershipParcels_MultiParts',
        fieldName,expression2,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('LandOwnershipParcels_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("LandOwnershipParcels","OwnershipReferenceNumber",
                    "LandOwnershipParcels_MultiParts","OwnershipReferenceNumber","Dup")
    with arcpy.da.UpdateCursor('LandOwnershipParcels','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('LandOwnershipParcels')
    print("Multipart Feature Present in LOP Layer")
else:
    if Pcount == MPcount:
        arcpy.Delete_management('LandOwnershipParcels_MultiParts')
        arcpy.Delete_management('LandOwnershipParcels')
        print('No Multipart Features in LOP Layer')

#Check for multipart features in Access Licence Data
Licence_count = arcpy.GetCount_management('EAA_Licences')
Lcount = int(Licence_count.getOutput(0))
print(str(Lcount) + ' Parcels in EAA Layer')
Licence_Multi_Count = arcpy.GetCount_management('EAA_Licences_MultiParts')
MLcount = int(Licence_Multi_Count.getOutput(0))
print(str(MLcount) + ' Parcels in Exploded EAA Layer')

if Lcount != MLcount:
    arcpy.AddField_management('EAA_Licences_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('EAA_Licences_MultiParts',
        fieldName,expression,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('EAA_Licences_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("EAA_Licences","LicenceID",
                    "EAA_Licences_MultiParts","LicenceID",'Dup')
    with arcpy.da.UpdateCursor('EAA_Licences','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('EAA_Licences_MultiParts')
    print("Multipart Feature Present in Access Licence Layer")
else:
    if Lcount == MLcount:
        arcpy.Delete_management('EAA_Licences_MultiParts')
        arcpy.Delete_management('EAA_Licences')
        print('No Multipart Features in Access Licence Layer')

#Check for multipart features in Ground Licence Data
GLicence_Count = arcpy.GetCount_management('GI_Licences')
Gcount = int(GLicence_Count.getOutput(0))
print(str(Gcount) + ' Parcels in GI Layer')
GLicence_Multi_count = arcpy.GetCount_management('GI_Licences_MultiParts')
MGcount = int(GLicence_Multi_count.getOutput(0))
print(str(MGcount) + ' Parcels in Exploded GI Layer')

if Gcount != MGcount:
    arcpy.AddField_management('GI_Licences_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('GI_Licences_MultiParts',
        fieldName,expression,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('GI_Licences_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("GI_Licences","LicenceID",
                    "GI_Licences_MultiParts","LicenceID","Dup")
    with arcpy.da.UpdateCursor('GI_Licences','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('GI_Licences_MultiParts')
    print("Multipart Feature Present in GI Layer")
else:
    if Gcount == MGcount:
        arcpy.Delete_management('GI_Licences_MultiParts')
        arcpy.Delete_management('GI_Licences')
        print('No Multipart Features in GI Licence')

#Check for multipart features in Noise Licence Data
NLicence_Count = arcpy.GetCount_management('NL_Licences')
NLCount = int(NLicence_Count.getOutput(0))
print(str(NLCount) + ' Parcels in NL Layer')
MNLicence_Count = arcpy.GetCount_management('NL_Licences_MultiParts')
MNL_Count = int(MNLicence_Count.getOutput(0))
print(str(MNL_Count) + ' Parcels in Exploded in NL Layer')

if NLCount != MNL_Count:
    arcpy.AddField_management('NL_Licences_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('NL_Licences_MultiParts',
        fieldName,expression,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('NL_Licences_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("NL_Licences","LicenceID",
                    "NL_Licences_MultiParts","LicenceID","Dup")
    with arcpy.da.UpdateCursor('NL_Licences','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('NL_Licences_MultiParts')
    print("Multipart Feature Present in NL Layer")
else:
    if NLCount == MNL_Count:
        arcpy.Delete_management('NL_Licences_MultiParts')
        arcpy.Delete_management('NL_Licences')
        print('No Multipart Features in NL Licence')

#Find out if overlapping or multipart features are present in each feature class
#then get status and export in CSV report
print("Producing QC Report")

duplicatelist = ['NL_Licences_Duplicate'
                ,'GI_Licences_Duplicate','EAA_Licences_Duplicate']


with arcpy.da.UpdateCursor('LandOwnershipParcels_Duplicate','COUNT_OwnershipReferenceNumber') as cursor:
    for row in cursor:
        if row[0] == 1:
                cursor.deleteRow()
for sum in duplicatelist:
    with arcpy.da.UpdateCursor(sum,'COUNT_LicenceID') as cursor:
        for row in cursor:
            if row[0] == 1:
                cursor.deleteRow()

duplicatelist2 = ['NL_Licences_Duplicate','LandOwnershipParcels_Duplicate',
                'GI_Licences_Duplicate','EAA_Licences_Duplicate']

for duplist2 in duplicatelist2:
    count = arcpy.GetCount_management(duplist2)
    print('Duplicates in ' + str(duplist2) + " " + str(count))
    if arcpy.management.GetCount(duplist2)[0] == "0":
        arcpy.Delete_management(duplist2)

fcs = arcpy.ListFeatureClasses()
QC_table = arcpy.ListTables()

if 'LandOwnershipParcels' in fcs:
    LOP_Multi = arcpy.GetCount_management('LandOwnershipParcels_MultiParts')
else:
    LOP_Multi = 'No'
if 'NL_Licences' in fcs:
    NL_MultiPart = arcpy.GetCount_management('NL_Licences_MultiParts')
else:
    NL_MultiPart = "No"
if 'GI_Licence' in fcs:
    GI_MultiPart = arcpy.GetCount_management('GI_Licence_MultiParts')
else:
    GI_MultiPart = "No"
if 'EAA_Licences' in fcs:
    Access_MultiPart = arcpy.GetCount_management('EAA_Licences_MultiParts')
else:
    Access_MultiPart = "No"
if 'LandOwnershipParcels_Int' in fcs:
    LOP_Overlap = arcpy.GetCount_management('LandOwnershipParcels_Int')
else:
    LOP_Overlap = "No"
if 'EAA_Licences_Int' in fcs:
    Access_Overlap = arcpy.GetCount_management('EAA_Licences_Int')
else:
    Access_Overlap = "No"
if 'GI_Licences_Int' in fcs:
    GI_Overlap = arcpy.GetCount_management('GI_Licences_Int')
else:
    GI_Overlap = "No"
if 'NL_Licences_Int' in fcs:
    NL_Overlap = arcpy.GetCount_management('NL_Licences_Int')
else:
    NL_Overlap = "No"
if 'LandOwnershipParcels_Duplicate' in QC_table:
    LOP_Dup = arcpy.GetCount_management('LandOwnershipParcels_Duplicate')
else:
    LOP_Dup = "No"
if 'NL_Licences_Duplicate' in QC_table:
    NL_Dup = arcpy.GetCount_management('NL_Licences_Duplicate')
else:
    NL_Dup = "No"
if 'GI_Licences_Duplicate' in QC_table:
    GI_Dup = arcpy.GetCount_management('GI_Licences_Duplicate')
else:
    GI_Dup = "No"
if 'EAA_Licences_Duplicate' in QC_table:
    EAA_Dup = arcpy.GetCount_management('EAA_Licences_Duplicate')
else:
    EAA_Dup = "No"

csv_output2 = WorkFolder + "\\" + "QC_Results_2B_Lot1.csv"

with open(csv_output2,'wb') as openCSV:
    a = csv.writer(openCSV)
    message = [['Feature','Overlaps', 'MultiPart','Duplicates']]
    a.writerows(message)
    message = [['Land Parcels', LOP_Overlap, LOP_Multi,LOP_Dup]]
    a.writerows(message)
    message = [['Access Licences', Access_Overlap, Access_MultiPart,EAA_Dup]]
    a.writerows(message)
    message = [['Noise Licences', NL_Overlap, NL_MultiPart,NL_Dup]]
    a.writerows(message)
    message = [['Ground Investigation Licences', GI_Overlap, GI_MultiPart, GI_Dup]]
    a.writerows(message)

SDE_Geodatabase = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde"

#Set Work Folder
print("Creating Local QC Copy of Phase 2B Lot 3")
GDB = "QC_Work_GDD_Leeds"
WorkGDD = WorkFolder + "\\" + GDB + ".gdb"
arcpy.env.workspace = SDE_Geodatabase
arcpy.CreateFileGDB_management(WorkFolder,GDB)

#set Calculator Variables
fieldName = "Dup"
expression = 'isDuplicateIndex( !LicenceID! )'
expression2 = 'isDuplicateIndex( !OwnershipReferenceNumber! )'
expression3 = 'isDuplicateIndex( !SHAPE_Area! )'
codeblock = """
UniqueDict = {}
def isDuplicateIndex(inValue):
    UniqueDict.setdefault(inValue,0)
    UniqueDict[inValue] += 1
    return UniqueDict[inValue]"""

#List feature classes in dataset
fc_List = arcpy.ListFeatureClasses("","","STATUTORY_PROCESSES")
QC_Features = ['LandOwnershipParcels','AccessLicences']

#Copy Licence and Parcel Feature Class to run QC on
for fc in QC_Features:
    if fc in QC_Features:
        arcpy.CopyFeatures_management(
            fc, os.path.join(WorkGDD,
                         os.path.basename(fc).split('\\')[0]))

#Re-set GDB to Work Folder
arcpy.env.workspace = WorkGDD
GDD_FC_List = arcpy.ListFeatureClasses()

#seperate licence layer into seperate licence types (NL, L, & G)
print("Copying Features To Desktop")
arcpy.FeatureClassToFeatureClass_conversion("AccessLicences",WorkGDD,"GI_Licences",
            "LicenceID LIKE 'G%'")
arcpy.FeatureClassToFeatureClass_conversion("AccessLicences",WorkGDD,"NL_Licences",
            "LicenceID LIKE'NL%'")
arcpy.FeatureClassToFeatureClass_conversion("AccessLicences",WorkGDD,"EAA_Licences",
            "LicenceID LIKE'L%'")
arcpy.Delete_management(WorkGDD + '\\' + 'AccessLicences')

fcs_revised = arcpy.ListFeatureClasses()

#Check for duplicates
print("Checking for duplicates")
LicenceList = ['GI_Licences','NL_Licences','EAA_Licences']
Ownership = ['LandOwnershipParcels']
#Run Initial QC Checks
for fc1 in fcs_revised:
    if fc1 in LicenceList:
        arcpy.Statistics_analysis(fc1,fc1 + '_Duplicate',"LicenceID COUNT","LicenceID")
    else:
        if fc1 in Ownership:
            arcpy.Statistics_analysis(fc1, fc1 + '_Duplicate',"OwnershipReferenceNumber COUNT",
                "OwnershipReferenceNumber")

print("Running Intersect and Multipart Checks")
for fcs in fcs_revised:
    arcpy.Intersect_analysis(fcs,fcs + "_Int","ALL","","INPUT")
    arcpy.MultipartToSinglepart_management(fcs,fcs + "_MultiParts")

#Check for overlapping features and if present export to GDD
OverlapList = arcpy.ListFeatureClasses()

for fcs2 in OverlapList:
    if "_Int" in fcs2:
        arcpy.MakeFeatureLayer_management(fcs2)
        if arcpy.management.GetCount(fcs2)[0] == "0":
            arcpy.Delete_management(fcs2)
            print("No Overlaps Present in " + fcs2)
        else:
            arcpy.AddField_management(fcs2,"Dup","SHORT")
            arcpy.CalculateField_management(fcs2,fieldName,expression3,
                "PYTHON_9.3", codeblock)
            with arcpy.da.UpdateCursor(fcs2,'Dup') as cursor:
                for row in cursor:
                    if row[0] == 1:
                        cursor.deleteRow()
            print("Overlaps Present in " + fcs2)

#Check for multipart features in Land Parcel Data
Parcel_Count = arcpy.GetCount_management('LandOwnershipParcels')
Pcount = int(Parcel_Count.getOutput(0))
print(str(Pcount) + ' Parcels in Original LOP Layer')
Parcel_Multi_Count = arcpy.GetCount_management('LandOwnershipParcels_MultiParts')
MPcount = int(Parcel_Multi_Count.getOutput(0))
print(str(MPcount) + ' Parcels in Exploded LOP Layer')

if Pcount != MPcount:
    arcpy.AddField_management('LandOwnershipParcels_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('LandOwnershipParcels_MultiParts',
        fieldName,expression2,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('LandOwnershipParcels_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("LandOwnershipParcels","OwnershipReferenceNumber",
                    "LandOwnershipParcels_MultiParts","OwnershipReferenceNumber","Dup")
    with arcpy.da.UpdateCursor('LandOwnershipParcels','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('LandOwnershipParcels_MultiParts')
    print("Multipart Feature Present in LOP Layer")
else:
    if Pcount == MPcount:
        arcpy.Delete_management('LandOwnershipParcels_MultiParts')
        arcpy.Delete_management('LandOwnershipParcels')
        print('No Multipart Features in LOP Layer')

#Check for multipart features in Access Licence Data
Licence_count = arcpy.GetCount_management('EAA_Licences')
Lcount = int(Licence_count.getOutput(0))
print(str(Lcount) + ' Parcels in EAA Layer')
Licence_Multi_Count = arcpy.GetCount_management('EAA_Licences_MultiParts')
MLcount = int(Licence_Multi_Count.getOutput(0))
print(str(MLcount) + ' Parcels in Exploded EAA Layer')

if Lcount != MLcount:
    arcpy.AddField_management('EAA_Licences_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('EAA_Licences_MultiParts',
        fieldName,expression,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('EAA_Licences_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("EAA_Licences","LicenceID",
                    "EAA_Licences_MultiParts","LicenceID",'Dup')
    with arcpy.da.UpdateCursor('EAA_Licences','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('EAA_Licences_MultiParts')
    print("Multipart Feature Present in Access Licence Layer")
else:
    if Lcount == MLcount:
        arcpy.Delete_management('EAA_Licences_MultiParts')
        arcpy.Delete_management('EAA_Licences')
        print('No Multipart Features in Access Licence Layer')

#Check for multipart features in Ground Licence Data
GLicence_Count = arcpy.GetCount_management('GI_Licences')
Gcount = int(GLicence_Count.getOutput(0))
print(str(Gcount) + ' Parcels in GI Layer')
GLicence_Multi_count = arcpy.GetCount_management('GI_Licences_MultiParts')
MGcount = int(GLicence_Multi_count.getOutput(0))
print(str(MGcount) + ' Parcels in Exploded GI Layer')

if Gcount != MGcount:
    arcpy.AddField_management('GI_Licences_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('GI_Licences_MultiParts',
        fieldName,expression,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('GI_Licences_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("GI_Licences","LicenceID",
                    "GI_Licences_MultiParts","LicenceID","Dup")
    with arcpy.da.UpdateCursor('GI_Licences','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('GI_Licences_MultiParts')
    print("Multipart Feature Present in GI Layer")
else:
    if Gcount == MGcount:
        arcpy.Delete_management('GI_Licences_MultiParts')
        arcpy.Delete_management('GI_Licences')
        print('No Multipart Features in GI Licence')

#Check for multipart features in Noise Licence Data
NLicence_Count = arcpy.GetCount_management('NL_Licences')
NLCount = int(NLicence_Count.getOutput(0))
print(str(NLCount) + ' Parcels in NL Layer')
MNLicence_Count = arcpy.GetCount_management('NL_Licences_MultiParts')
MNL_Count = int(MNLicence_Count.getOutput(0))
print(str(MNL_Count) + ' Parcels in Exploded in NL Layer')

if NLCount != MNL_Count:
    arcpy.AddField_management('NL_Licences_MultiParts',"Dup","SHORT")
    arcpy.CalculateField_management('NL_Licences_MultiParts',
        fieldName,expression,"PYTHON_9.3", codeblock)
    with arcpy.da.UpdateCursor('NL_Licences_MultiParts','Dup') as cursor:
            for row in cursor:
                if row[0] == 1:
                    cursor.deleteRow()
    arcpy.JoinField_management("NL_Licences","LicenceID",
                    "NL_Licences_MultiParts","LicenceID","Dup")
    with arcpy.da.UpdateCursor('NL_Licences','Dup') as cursor:
        for row in cursor:
            if row[0] is None:
                    cursor.deleteRow()
    arcpy.Delete_management('NL_Licences_MultiParts')
    print("Multipart Feature Present in NL Layer")
else:
    if NLCount == MNL_Count:
        arcpy.Delete_management('NL_Licences_MultiParts')
        arcpy.Delete_management('NL_Licences')
        print('No Multipart Features in NL Licence')

#Find out if overlapping or multipart features are present in each feature class
#then get status and export in CSV report
print("Producing QC Report")

duplicatelist = ['NL_Licences_Duplicate'
                ,'GI_Licences_Duplicate','EAA_Licences_Duplicate']


with arcpy.da.UpdateCursor('LandOwnershipParcels_Duplicate','COUNT_OwnershipReferenceNumber') as cursor:
    for row in cursor:
        if row[0] == 1:
                cursor.deleteRow()
for sum in duplicatelist:
    with arcpy.da.UpdateCursor(sum,'COUNT_LicenceID') as cursor:
        for row in cursor:
            if row[0] == 1:
                cursor.deleteRow()

duplicatelist2 = ['NL_Licences_Duplicate','LandOwnershipParcels_Duplicate',
                'GI_Licences_Duplicate','EAA_Licences_Duplicate']

for duplist2 in duplicatelist2:
    count = arcpy.GetCount_management(duplist2)
    print('Duplicates in ' + str(duplist2) + " " + str(count))
    if arcpy.management.GetCount(duplist2)[0] == "0":
        arcpy.Delete_management(duplist2)

fcs = arcpy.ListFeatureClasses()
QC_table = arcpy.ListTables()

if 'LandOwnershipParcels' in fcs:
    LOP_Multi = arcpy.GetCount_management('LandOwnershipParcels')
else:
    LOP_Multi = 'No'
if 'NL_Licences' in fcs:
    NL_MultiPart = arcpy.GetCount_management('NL_Licences')
else:
    NL_MultiPart = "No"
if 'GI_Licence' in fcs:
    GI_MultiPart = arcpy.GetCount_management('GI_Licence')
else:
    GI_MultiPart = "No"
if 'EAA_Licences' in fcs:
    Access_MultiPart = arcpy.GetCount_management('EAA_Licences')
else:
    Access_MultiPart = "No"
if 'LandOwnershipParcels_Int' in fcs:
    LOP_Overlap = arcpy.GetCount_management('LandOwnershipParcels_Int')
else:
    LOP_Overlap = "No"
if 'EAA_Licences_Int' in fcs:
    Access_Overlap = arcpy.GetCount_management('EAA_Licences_Int')
else:
    Access_Overlap = "No"
if 'GI_Licences_Int' in fcs:
    GI_Overlap = arcpy.GetCount_management('GI_Licences_Int')
else:
    GI_Overlap = "No"
if 'NL_Licences_Int' in fcs:
    NL_Overlap = arcpy.GetCount_management('NL_Licences_Int')
else:
    NL_Overlap = "No"
if 'LandOwnershipParcels_Duplicate' in QC_table:
    LOP_Dup = arcpy.GetCount_management('LandOwnershipParcels_Duplicate')
else:
    LOP_Dup = "No"
if 'NL_Licences_Duplicate' in QC_table:
    NL_Dup = arcpy.GetCount_management('NL_Licences_Duplicate')
else:
    NL_Dup = "No"
if 'GI_Licences_Duplicate' in QC_table:
    GI_Dup = arcpy.GetCount_management('GI_Licences_Duplicate')
else:
    GI_Dup = "No"
if 'EAA_Licences_Duplicate' in QC_table:
    EAA_Dup = arcpy.GetCount_management('EAA_Licences_Duplicate')
else:
    EAA_Dup = "No"

csv_output3 = WorkFolder + "\\" + "QC_Results_2B_Lot3.csv"

with open(csv_output3,'wb') as openCSV:
    a = csv.writer(openCSV)
    message = [['Feature','Overlaps', 'MultiPart','Duplicates']]
    a.writerows(message)
    message = [['Land Parcels', LOP_Overlap, LOP_Multi,LOP_Dup]]
    a.writerows(message)
    message = [['Access Licences', Access_Overlap, Access_MultiPart,EAA_Dup]]
    a.writerows(message)
    message = [['Noise Licences', NL_Overlap, NL_MultiPart,NL_Dup]]
    a.writerows(message)
    message = [['Ground Investigation Licences', GI_Overlap, GI_MultiPart, GI_Dup]]
    a.writerows(message)


#list connections to relevent fc on SDE for Hs2A
#Hs2A
Hs2A_Licence_Amends = r"Database Connections\HS2-Phase2A-Manchester-GSS.sde\HS2phase2A.GSS.STATUTORY_PROCESSES\HS2phase2A.GSS.AccessLicenceAmends"
Hs2A_Parcel_Amends = r"Database Connections\HS2-Phase2A-Manchester-GSS.sde\HS2phase2A.GSS.STATUTORY_PROCESSES\HS2phase2A.GSS.LandOwnershipParcelAmends"

#GetParcel and licence count
HS2a_Parcelcount = [row for row in arcpy.da.SearchCursor(Hs2A_Parcel_Amends,'ActionedBy',"ActionedBy IS NULL")]
p_count2a = len(HS2a_Parcelcount)
HS2a_Licencecount = [row for row in arcpy.da.SearchCursor(Hs2A_Licence_Amends,'ActionedBy',"ActionedBy IS NULL")]
l_count2a = len(HS2a_Licencecount)

#QC to delete
Hs2A_Parcel_Count = str(str(p_count2a) + " outstanding parcel amends")
Hs2A_Licence_Count = str(str(l_count2a) + " outstanding licence amends")

#list connections to relevent fc on SDE for Hs2B Lot 1
#Hs2B Lot 1
Hs2B_L1_Licence_Amends = r"Database Connections\HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde\HS2phase2B.GSS.STATUTORY_PROCESSES\HS2phase2B.GSS.AccessLicenceAmends"
Hs2B_L1_ParcelAmends = r"Database Connections\HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde\HS2phase2B.GSS.STATUTORY_PROCESSES\HS2phase2B.GSS.LandOwnershipParcelAmends"

#GetParcel and licence count
Hs2B_L1_Parcelcount = [row for row in arcpy.da.SearchCursor(Hs2B_L1_ParcelAmends,'ActionedBy',"ActionedBy IS NULL")]
p_count2B_L1 = len(Hs2B_L1_Parcelcount)
Hs2B_L1_Licencecount = [row for row in arcpy.da.SearchCursor(Hs2B_L1_Licence_Amends,'ActionedBy',"ActionedBy IS NULL")]
l_count2B_L1 = len(Hs2B_L1_Licencecount)

#list connections to relevent fc on SDE for Hs2B Lot 3
#Hs2B Lot 1
Hs2B_L3_Licence_Amends = r" Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde\HS2phase2B_WSP.GSS.STATUTORY_PROCESSES\HS2phase2B_WSP.GSS.AccessLicenceAmends"
Hs2B_L3_ParcelAmends = r"Database Connections\HS2-Phase2B-Leeds-L3L4-Lot3-GSS.sde\HS2phase2B_WSP.GSS.STATUTORY_PROCESSES\HS2phase2B_WSP.GSS.LandOwnershipParcelAmends"

#GetParcel and licence count
Hs2B_L3_Parcelcount = [row for row in arcpy.da.SearchCursor(Hs2B_L3_ParcelAmends,'ActionedBy',"ActionedBy IS NULL")]
p_count2B_L3 = len(Hs2B_L3_Parcelcount)
Hs2B_L3_Licencecount = [row for row in arcpy.da.SearchCursor(Hs2B_L3_Licence_Amends,'ActionedBy',"ActionedBy IS NULL")]
l_count2B_L3 = len(Hs2B_L3_Licencecount)

#Create counts for Hs2 amends layers
Hs2B_Parcel_Count = str(str(p_count2B_L1) + " outstanding parcel amends")
Hs2B_Licence_Count = str(str(l_count2B_L1) + " outstanding licence amends")
Hs2B_L3_Parcel_Count = str(str(p_count2B_L3) + " outstanding parcel amends")
Hs2B_L3_Licence_Count = str(str(l_count2B_L3) + " outstanding licence amends")

#Copy GDBs to shared drive
arcpy.env.workspace = WorkFolder
Copy_List = arcpy.ListWorkspaces("","FileGDB")
print('copying GDB to Server')
for gds in Copy_List:
    Gdd_name = os.path.basename(gds).split('\\')[0]
    Copyname = WorkFolder2 + "\\" + Gdd_name
    arcpy.Copy_management(gds,Copyname)

print('Copy complete')

#Generate output email
print('Sending QC email')

subject = "Hs2A & Hs2B Lot 1 QC Report - Python draft v1 "

text = (r"""Hello All<br><br>
     Please find summaries for Hs2A, Hs2B Lot 1 & Hs2B Lot3:<br><br>
     Phase 2A:<br>
     {}<br>{}<br><br>
     Phase 2B Lot 1:
     <br>{}<br>{}<br><br>
     Phase 2B Lot 3:
     <br>{}<br>{}<br><br>
     Here is the <a href='{}'>GDB Location</a> for fixing.<br><br>
     Kind regards,<br><br>
     <b>Kane Russell</b><br>
     GIS Consultant<br>Bsc,Msc, FRGS""".format(Hs2A_Parcel_Count,Hs2A_Licence_Count,Hs2B_Parcel_Count,Hs2B_Licence_Count,Hs2B_L3_Parcel_Count,Hs2B_L3_Licence_Count,WorkFolder2))

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'Kane.Russell@wsp.com; Adil.Toorawa@wsp.com; Ollie.Brown@wsp.com; Ross.Goodacre@wsp.com; Patrick.Reynolds@wsp.com; Kuhu.Dahiya@wsp.com; Boglarka.Csomos@wsp.com; Vasiliki.Ketsetzopoulou@wsp.com; Shrabanti.Hira@wsp.com; Alexandra.Hajok@wsp.com; David.Evans2@wsp.com'
mail.Subject = subject
mail.HtmlBody = text
mail.Attachments.Add(csv_output)
mail.Attachments.Add(csv_output2)
mail.Attachments.Add(csv_output3)
mail.Display(False)
mail.send

print("email sent, removing scratch folder")

#Remove Folder
Removing_List = arcpy.ListWorkspaces(WorkFolder)

for del_gdb in Removing_List:
    remov_list = arcpy.ListFeatureClasses("","",del_gdb)
    for del_Fc in remov_list:
        arcpy.DeleteFeatures_management()
    remov_tab = arcpy.ListTables(del_gdb)
    for re_tabl in Removing_List:
        arcpy.Delete_management(re_tabl)

shutil.rmtree(WorkFolder)
print('Script complete')