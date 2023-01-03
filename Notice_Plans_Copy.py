
#notice_nps v5.5 / ArcGIs 10.3.1
#Notice production from NPS csv file
#Creates areas and extents to append to SDE feature classes
#VM @ 2017 / GSS WSP

#HEADING
#general statements
import arcpy
from arcpy import mapping
import csv
import string
import ConversionUtils
import shutil
import os

arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(27700)
arcpy.AddMessage("")
arcpy.AddMessage("Loading layers...")


#paths and databases
arcpy.env.workspace = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Noitce_Plan_Tool\notices\HS2temp_VM.gdb'
tempfolder = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Noitce_Plan_Tool\notices\HS2temp_VM.gdb'

#####
LAP = r'C:\Users\UKPXR011\Documents\ArcGIS\FeatureServiceLocalEdits\HS2_Phase1_South_HS2_Phase2a_Feature\fs894B94638F584A7B967B73D8D31E0578.gdb\LANDACQUISITIONPARCELS'

#####
districts =r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Noitce_Plan_Tool\notices\HS2temp_VM.gdb\Districts_2a'
vessel = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Noitce_Plan_Tool\notices\HS2temp_VM.gdb\NPvessel'
tmply = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Noitce_Plan_Tool\notices\HS2temp_VM.gdb\templayer'


#tool parameters
csvfile= r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\csv\A104_076.csv'
outputfc = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Noitce_Plan_Tool\notices\HS2temp_VM.gdb\newnps'
outputex = r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Noitce_Plan_Tool\notices\HS2temp_VM.gdb\newnpsextents'
outputex_combined =  r'C:\Users\UKPXR011\Desktop\Current Work\2A\Notice Plans\Noitce_Plan_Tool\notices\HS2temp_VM.gdb\newnpsextents_Combined'

pro = 'PR'
che = 'HS'
prod = "'{0}'" .format(pro)
chec = "'{0}'" .format(che)




#FUNCTIONS

arcpy.AddMessage("Loading functions...")

#date function
def add_date():
	import time
	return time.strftime("%d/%m/%Y")
date = add_date()
dat = "'{0}'" . format (date)


#scale functions


def scc(lenX,lenY,type):
	if (lenX < 350) and (lenY < 200):
		sc = 1250
	elif (lenX < 980) and (lenY < 610):
		sc = 2500
        elif (lenX < 1400) and (lenY < 930):
		sc = 3750
	elif (lenX < 1950) and (lenY < 1250):
		sc = 5000
	elif (lenX < 2925) and (lenY < 1875):
		sc = 7500
	else:
		sc = 0
	return sc

def scal():

	arcpy.AddGeometryAttributes_management(fc, "EXTENT","METERS")
	arcpy.CalculateField_management (fc, "LX", "!EXT_MAX_X!- !EXT_MIN_X!", "PYTHON_9.3")
	arcpy.CalculateField_management (fc, "LY", "!EXT_MAX_Y!- !EXT_MIN_Y!", "PYTHON_9.3")

	with arcpy.da.UpdateCursor(fc, ["DDPScale","LX","LY","NoticeType"]) as cursor:
		for row in cursor:
			row[0] = scc (row[1],row[2],row[3])
			cursor.updateRow(row)
	del cursor


#calculate fields unique values
def calcuniq():
	arcpy.CalculateField_management (fc, "ContactID", namestr, "PYTHON_9.3")
	arcpy.CalculateField_management (fc, "NPNo", noticestr, "PYTHON_9.3")
	arcpy.CalculateField_management (fc, "ExportID", "!NPNo!", "PYTHON_9.3")
	arcpy.CalculateField_management (fc, "NoticeType", schedstr, "PYTHON_9.3")

#calculate fields general values
def calcgeneral():
	arcpy.CalculateField_management (fc, "Rev", "'0.1'", "PYTHON_9.3")
	arcpy.CalculateField_management (fc, "DateProd", dat,'PYTHON')
	arcpy.CalculateField_management (fc, "ProdBy", prod, "PYTHON_9.3")
	arcpy.CalculateField_management (fc, "ChkdBy", chec, "PYTHON_9.3")



#calculate the location
def areacalc ():
	areaname = ""
	arcpy.SelectLayerByLocation_management ("distr", "INTERSECT",fc)
	alist = []
	rows = arcpy.SearchCursor("distr")
	for row in rows:
		alist.append(row.getValue("NAME"))
	del rows
	areastr = ""
	for a in alist:
		areastr = areastr + str(a)
		areaname = "'{0}'".format (areastr)
		arcpy.AddMessage(areaname)
		areastr = areastr + " / "
        print areaname

	arcpy.CalculateField_management (fc, "District", areaname, "PYTHON_9.3")


#PROCESSING

arcpy.AddMessage("Creating feature layers...")
#creation of temp layers and emptying the vessel
arcpy.MakeFeatureLayer_management(LAP,"NPtemp")
arcpy.MakeFeatureLayer_management(districts,"distr")
arcpy.DeleteRows_management(vessel)

#reading the csv file and creating a matrix
arcpy.AddMessage("Reading csv...")
matrix = []
with open(csvfile, 'rb') as f:
    next (f)
    reader = csv.reader(f)
    matrix = map(list, reader)

#iterating through rows ang getting values
arcpy.AddMessage("Processing...")
for m in matrix:
	party = m[0]
	name = m[1]
	notice = m[2]
	sched = m[3]
	landreq = m[4]
	laanum = m[5]
	lapid = m[6]

	arcpy.AddMessage("Notice: {0} for {1}" .format(notice, party))
	namest = name.replace ("'","\\'")
	namestr = "'{0}'" .format (namest)
	noticestr= "'{0}'" .format (notice)
	schedstr= "'{0}'" .format (sched)
	newlapid = string.replace(lapid,"LAP","")
	lapidstr = string.replace(newlapid,"; ","','")
	laastr = "'{0}'" .format (laanum)

	query = "LAPID IN ('{0}')" .format (lapidstr)

	arcpy.SelectLayerByAttribute_management("NPtemp", "NEW_SELECTION", query)

	arcpy.DeleteRows_management(tmply)
	arcpy.Append_management ("NPtemp", tmply, "NO_TEST")

	arcpy.AddMessage("TMPCM to TMPEX")
	query = "LRType = 'TMPCM'"
	arcpy.MakeFeatureLayer_management(tmply,"newlay")
	fc = "newlay"
	arcpy.SelectLayerByAttribute_management(fc, "NEW_SELECTION", query)
	arcpy.CalculateField_management (fc, "LRType", "'TMPEX'", "PYTHON_9.3")
	arcpy.SelectLayerByAttribute_management(fc, "CLEAR_SELECTION")


	#fc = "templayer"
	arcpy.AddMessage("Calculating fields")
	calcuniq()

	#arcpy.AddMessage("Calculating districts")
	areacalc()
	arcpy.Append_management (fc, vessel, "NO_TEST")


arcpy.AddMessage("Calculating general fields...")
fc = vessel
calcgeneral()
scal()

arcpy.AddMessage("Compiling...")
arcpy.CopyFeatures_management (vessel, outputfc)
arcpy.CopyFeatures_management (vessel, outputex)

dissolve_Fields = ['LAAID', 'ContactID', 'NPNo', 'LRType', u'Rev', 'DateProd', 'ProdBy', 'ChkdBy', 'NoticeType', 'ExportID', 'District', 'Scale']


arcpy.Dissolve_management(outputex,outputex_combined,dissolve_Fields)


with arcpy.da.UpdateCursor(outputex_combined, ["SHAPE@", "NPNo", "Scale"]) as updateRows:

    for updateRow in updateRows:
        extent = updateRow[0].extent
        #LAA_ID = ("{0}".format(row[1]))
            # Create a polygon geometry
        array = arcpy.Array([arcpy.Point(extent.XMin, extent.YMin), arcpy.Point(extent.XMax, extent.YMin),
                                 arcpy.Point(extent.XMax, extent.YMax), arcpy.Point(extent.XMin, extent.YMax)])
        polygon = arcpy.Polygon(array)
        polygon_area = float(polygon.area)
        if polygon_area < 100000.00: #140767.95:
            Intial_Scale = '1250'
            updateRow[2] = Intial_Scale
        elif 100000.01 < polygon_area < 350000.00:
            Intial_Scale = '2500'
            updateRow[2] = Intial_Scale
        elif 350000.01 < polygon_area < 1800000.00:
            Intial_Scale = '5000'
            updateRow[2] = Intial_Scale
        elif 1800000.01 < polygon_area < 4500000.00:
            Intial_Scale = '7500'
            updateRow[2] = Intial_Scale
        else:
            Intial_Scale = '10000'
            updateRow[2] = Intial_Scale

        updateRows.updateRow(updateRow)








