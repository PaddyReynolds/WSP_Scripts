# Import system modules
import arcpy
import pandas as pd
from datetime import *

#Capture start time of script
start = datetime.now()
print 'Create NPS: %s\n' % (start)

# Set global variables
arcpy.env.overwriteOutput = True

# Change the workspace to where you would like the Project folder to be saved
workspace = r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS'

# Change the name of the folder to the Project name
projectname = "NPS_Refresh"

# Create a container folder within the specified workspace containing the folder specified as Project Name above and dated to current date time
createprojectfolder = arcpy.CreateFolder_management(workspace, projectname+"_"+str(datetime.today().strftime('%Y%m%d_%H%M%S')))

# Local Variables
npsID = "TITLE_NO"

# Create required FGDBs for Output and Working data
Output = arcpy.CreateFileGDB_management(createprojectfolder,"Output.gdb")
Working = arcpy.CreateFileGDB_management(createprojectfolder,"Working.gdb")

# Inputs
InputAOI = r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS\Scratch.gdb\CP3_SG_OLD_1'
##inputNPS = r"C:\Users\ukodb001\Desktop\Tasks\2020\SOP_Creation\Incoming\National_Polygon_Service_January2020_FullSupply\National_Polygon_Service_January2020_FullSupply\National_Polygon_Service_January2020_FullSupply.gdb\GEODATA\NPD_January2020_FullSupply"
inputNPS = r'C:\Users\UKPXR011\Desktop\Safeguarding\NPS\National_Polygon_Service_January2020_FullSupply\National_Polygon_Service_January2020_FullSupply_1.gdb\GEODATA\L3L4_NPS'

# Process 1 - To ascertain which titles intersect the AOI
intersectNPS1 = arcpy.Intersect_analysis([InputAOI,inputNPS], str(Working)+"\NPS_Intersect1", "ALL", "", "INPUT")
with arcpy.da.SearchCursor(intersectNPS1, ["TITLE_NO","REC_STATUS"],"""REC_STATUS <> 'D'""") as cursor:
    selected_NPS1 = sorted({row[0] for row in cursor})
liststring1 = ",".join("'%s'" % r for r in selected_NPS1)
whereclause1 = ("""TITLE_NO in(%s)""" % liststring1)
selectcurrentNPS1 = arcpy.Select_analysis(inputNPS, str(Working)+"\Current_NPS1", whereclause1)

# Process 2 - To asertain which titles fall within those titles intersecting the AOI but do not directly intersect with it
NPSDissolve = arcpy.Dissolve_management(selectcurrentNPS1, str(Working)+"\NPS_Dissolve")
intersectNPS2 = arcpy.Intersect_analysis([NPSDissolve,inputNPS], str(Working)+"\NPS_Intersect2", "ALL", "", "INPUT")
with arcpy.da.SearchCursor(intersectNPS2, ["TITLE_NO","REC_STATUS"],"""REC_STATUS <> 'D'""") as cursor:
    selected_NPS2 = sorted({row[0] for row in cursor})
liststring2 = ",".join("'%s'" % r for r in selected_NPS2)
whereclause2 = ("""TITLE_NO in(%s)""" % liststring2)
selectcurrentNPS2 = arcpy.Select_analysis(inputNPS, str(Output)+"\NPS", whereclause2)

#Capture end time of script
print 'NPS Creation finished in: %s\n\n' % (datetime.now() - start)
