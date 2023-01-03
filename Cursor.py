#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     19/12/2019
# Copyright:   (c) UKPXR011 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
from datetime import *

#Capture start time of script
start = datetime.now()
print 'Script: %s\n' % (start)

#Set global variables
arcpy.env.overwriteOutput = True

#Change the workspace to where you would like the Project folder to be saved
workspace = r"C:\Users\UKPXR011\Desktop\Stats\CommunityBoundaryStats"

txt_Path = os.path.dirname(os.path.abspath(workspace))

fc = r'C:\Users\UKPXR011\Desktop\Stats\CommunityBoundaryStats\CommBoundaryStats.gdb\STATUTORY_PROCESSES\AccessLicences'
fc2 = r'C:\Users\UKPXR011\Desktop\Stats\CommunityBoundaryStats\CommBoundaryStats.gdb\HS2_HSTWO_CommunityAreaBoundary_Ply'

issued = len(list(i for i in arcpy.da.SearchCursor(fc, ['Status'],"Status = 'Agreed'")))
print issued

#LoopThrough Community Boundaries
#cursor = arcpy.SearchCursor(fc2,['CA'])
#with arcpy.da.SearchCursor(fc2,['CA']) as cursor:
 #   for row in cursor:
  #      print str(row[0])