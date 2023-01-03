import arcpy
import os
import math
from datetime import *

arcpy.env.overwriteOutput = True

#Capture start time of script
start = datetime.now()
print 'Script: %s\n' % (start)

#Set global variables
arcpy.env.overwriteOutput = True

#Change the workspace to where you would like the Project folder to be saved
workspace = r"C:\Users\UKPXR011\Desktop\Stats\communityBoundaryStats"

#InputFeatureClasses
fc = r'C:\Users\UKPXR011\Desktop\Stats\CommunityBoundaryStats\CommBoundaryStats.gdb\STATUTORY_PROCESSES\AccessLicences'
fc2 = r'C:\Users\UKPXR011\Desktop\Stats\CommunityBoundaryStats\CommBoundaryStats.gdb\HS2_HSTWO_CommunityAreaBoundary_Ply'

#Empty List to hold the statistics
stats = []

# Create required FGDBs for Output,and Working data
Output = arcpy.CreateFileGDB_management(workspace,"Output")
Working = arcpy.CreateFileGDB_management(workspace,"Working")


# get only issued licenses
issuedLicenceName= str(Working)+"\\Issued_Licenses"
IssuedLicenceQuery = "Status NOT IN ( 'Not Issued', 'No Longer Required')"
issuedLicence=arcpy.Select_analysis(fc,issuedLicenceName,IssuedLicenceQuery)
#list features in community boundaries

with arcpy.da.SearchCursor(fc2,['CA']) as cursor:
    for row in cursor:

        #comBoundary = str(row[0])
        query = "CA =" +"'"+str(row[0])+"'"
        output = str(Working)+"\\"+ str(row[0])+"Intersect"
        dissove = str(Working) +"\\"+str(row[0])+"_Dissolve"
        dissolvefields = ["LicenceID", "Status"]
        comunityBoundary = arcpy.Select_analysis(fc2,str(Working)+"\\" +str(row[0]),query)
        issued = 0
        # intersect dissolve access licence
        intersectIssuedComunityBoundary = arcpy.Intersect_analysis([comunityBoundary,issuedLicence], output, "ALL", "", "INPUT")

        fc3= arcpy.Dissolve_management(intersectIssuedComunityBoundary,dissove,dissolvefields)
        # get total number of licenses and then agreed licenses
        #total = len(list(i for i in cursor2))

        total =  float(len(list(i for i in arcpy.da.SearchCursor(fc3, ['Status']))))
        issued = float(len(list(i for i in arcpy.da.SearchCursor(fc3, ['Status'],"Status = 'Agreed'"))))
        percentage = ((issued/total)*100)
        comPercent = str(cursor[0]) + " Agreed Percentage = "+str(percentage)+"%"
        print comPercent
        stats.append(comPercent)


with open(os.path.join(workspace, "CommunityBoundaryStats.txt"), "w") as f:
    for item in stats:
        f.write("%s\n" % item)


print "Script Complete"
