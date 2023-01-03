#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     17/08/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

fc1 = LAPS

fc2 = plots

fc3 = LAPS-Plots relates

fc4 = scracth + "LAP_Plots_Intersect"

fc5 = scracth + "LAP_Plots_Dissolve"

DissolveFields = []
IntersectFields = ['LAPID', 'SHAPE@']
nameField = 'Shape_Area'
UpdateFields = ['LAPID','Include']
searchFields = ['LAPID','Include','GlobalID', #contactID]
RelateFields = [LAPGlobID, PlotGlobID]

#Add a field to the LAPS to Mark if a LAP intersects a plot by more than 2m

#Intersect and Dissolve PLOTS and LAPS dissolve my plot number parish and LAP ID, Removed

arcpy.Intersect_analysis([fc1,fc2],fc4)
arcpy.Dissolve_management(fc4, fc5,DissolveFields)

expression = arcpy.AddFieldDelimiters(fc1, nameField) + ' =<2'

#Build a dictionary of LAPS that intersect Plots by more than 2m
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(fc5,IntersectFields,where_clause=expression)}

#Search cursor to make a list of global ID's where Yes
LAP_GlobalID = []
NoContactId = []


with arcpy.da.SearchCursor(fc1,searchFields) as cursor:
    for i in cursor:

        keyValue = i[0]
        if keyValue in valueDict:
            LAP_GlobalID.append(i[2])
                if i[3] is None:
                    NoContactId.append(i[2])

#Search Cursor to check if Yes does it have a valid relate to a plot and if the Plot is removed
#List thoes that should have a relate and do not, thoes that have a relate but not contact ID, thoes that are related to removed plots

with arcpy.da.SearchChursor(fc3,[RelateFields])



#excel wizardry for reports.