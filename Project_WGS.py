# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Project_WGS.py
# Created on: 2019-12-20 15:56:55.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


# Local variables:
SampleRoads = "C:\\Users\\UKPXR011\\Desktop\\Street_View\\Scratch.gdb\\SampleRoads"
SampleRoads_Project = "C:\\Users\\UKPXR011\\Documents\\ArcGIS\\Default.gdb\\SampleRoads_Project"

# Process: Project
arcpy.Project_management(SampleRoads, SampleRoads_Project, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "OSGB_1936_To_WGS_1984_Petroleum", "PROJCS['British_National_Grid',GEOGCS['GCS_OSGB_1936',DATUM['D_OSGB_1936',SPHEROID['Airy_1830',6377563.396,299.3249646]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',400000.0],PARAMETER['False_Northing',-100000.0],PARAMETER['Central_Meridian',-2.0],PARAMETER['Scale_Factor',0.9996012717],PARAMETER['Latitude_Of_Origin',49.0],UNIT['Meter',1.0]]", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")

