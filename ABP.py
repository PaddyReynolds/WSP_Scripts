# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# ABP.py
# Created on: 2020-08-04 15:59:14.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


# Local variables:
ADM_ORDSU_ABP_ID99_Trailer_Tbl = "C:\\Users\\UKPXR011\\Desktop\\Current Work\\Super Tracker\\GIS\\ABP\\HS2-HS2-GI-GDD-000-001075_P09 - Copy\\ABP_1_201908.gdb\\ABP_1_201908.gdb\\ADM_ORDSU_ABP_ID99_Trailer_Tbl"
ADM_ORDSU_ABP_ID99_Trailer_Tbl__2_ = ADM_ORDSU_ABP_ID99_Trailer_Tbl
ADM_ORDSU_ABP_ID21_BLPU_Pt = "ADM_ORDSU_ABP_ID21_BLPU_Pt"

# Process: Join Field
arcpy.JoinField_management(ADM_ORDSU_ABP_ID99_Trailer_Tbl, "", ADM_ORDSU_ABP_ID21_BLPU_Pt, "", "")

