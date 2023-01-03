# File name: ProcessABP.py
# Author: Ollie Brown
# Date created: 20190918
# Date last modified: N/A
# Python Version: 2.7.13

# USAGE NOTES - This script does not select the ABP within the area you require or remove non-addressable records, it does not add an index to the UPRN field of the address points to
# speed up processing times. These steps must be performed prior to using this tool. This tool is intended for use on data which has never been processed that has been received fom HS2.

# Import system modules
import arcpy
from datetime import *

#Capture start time of script
start = datetime.now()
print 'ABP Processing Started: %s\n' % (start)

# Set global variables
arcpy.env.overwriteOutput = True

# Change the workspace to where you would like the Project folder to be saved
workspace = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\ABP"

# Change the name of the folder to the Project name
projectname = "Address_Base_Premium_Processing"

# Create a container folder within the specified workspace containing the folder specified as Project Name above and dated to current date time
createprojectfolder = arcpy.CreateFolder_management(workspace, projectname+"_"+str(datetime.today().strftime('%Y%m%d_%H%M%S')))

# Create required FGDBs for Output, WebGIS storage and Working data
Output = arcpy.CreateFileGDB_management(createprojectfolder,"Output.gdb")
Working = arcpy.CreateFileGDB_management(createprojectfolder,"Working.gdb")

# List Input Feature Class
abpinput = r"C:\Users\UKPXR011\Desktop\Current Work\2A\Safeguarding\ABP\ABP.gdb\AddressableAddressPoints2aHS2"

# List Input Tables
id11 = r"C:\Users\UKPXR011\Desktop\Current Work\ABP\ABP_Epoch79_2\AB_TablesEpoch79_2.gdb\ADM_ORDSU_ABP_ID11_Street_Tbl" # Street table
id15 = r"C:\Users\UKPXR011\Desktop\Current Work\ABP\ABP_Epoch79_2\AB_TablesEpoch79_2.gdb\ADM_ORDSU_ABP_ID15_StreetDesc_Tbl" # Street description table
id24 = r"C:\Users\UKPXR011\Desktop\Current Work\ABP\ABP_Epoch79_2\AB_TablesEpoch79_2.gdb\ADM_ORDSU_ABP_ID24_LPI_Tbl" # LPI table
id28 = r"C:\Users\UKPXR011\Desktop\Current Work\ABP\ABP_Epoch79_2\AB_TablesEpoch79_2.gdb\ADM_ORDSU_ABP_ID28_DPA_Tbl" # DPA table
id31 = r"C:\Users\UKPXR011\Desktop\Current Work\ABP\ABP_Epoch79_2\AB_TablesEpoch79_2.gdb\ADM_ORDSU_ABP_ID31_Org_Tbl" # Organisation table
id32 = r"C:\Users\UKPXR011\Desktop\Current Work\ABP\ABP_Epoch79_1\AB_TablesEpoch79_1.gdb\ADM_ORDSU_ABP_ID32_Class_Tbl" # Classification table
'''
# Alter id11 table fields
id11fieldlist = arcpy.ListFields(id11)
for field in id11fieldlist: #loop through each field
    if field.name not in ("OBJECTID"):
        arcpy.AlterField_management(id11, field.name, "ID11_"+field.name)
print "ID11 table fields altered"

# Alter id25 table fields
id15fieldlist = arcpy.ListFields(id15)
for field in id15fieldlist: #loop through each field
    if field.name not in ("OBJECTID"):
        arcpy.AlterField_management(id15, field.name, "ID15_"+field.name)
print "ID15 table fields altered"

# Alter id24 table fields
id24fieldlist = arcpy.ListFields(id24)
for field in id24fieldlist: #loop through each field
    if field.name not in ("OBJECTID"):
        arcpy.AlterField_management(id24, field.name, "ID24_"+field.name)
print "ID24 table fields altered"
'''

# Alter id28 table fields
id28fieldlist = arcpy.ListFields(id28)
for field in id28fieldlist: #loop through each field
    if field.name not in ("OBJECTID"):
        arcpy.AlterField_management(id28, field.name, "ID28_"+field.name)
print "ID28 table fields altered"

'''
# Alter id31 table fields
id31fieldlist = arcpy.ListFields(id31)
for field in id31fieldlist: #loop through each field
    if field.name not in ("OBJECTID"):
        arcpy.AlterField_management(id31, field.name, "ID31_"+field.name)
print "ID31 table fields altered"

# Alter id31 table fields
id32fieldlist = arcpy.ListFields(id32)
for field in id32fieldlist: #loop through each field
    if field.name not in ("OBJECTID"):
        arcpy.AlterField_management(id31, field.name, "ID32_"+field.name)
print "ID32 table fields altered"
'''
#Capture end time of script
print 'Safeguarding finished in: %s\n\n' % (datetime.now() - start)
