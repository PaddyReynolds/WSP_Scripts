# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Selction.py
# Created on: 2019-08-19 15:21:21.00000
#   (generated by ArcGIS/ModelBuilder)
# Description:
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


# Local variables:
Output_Feature_Class = ""

# Process: Calculate Field
arcpy.CalculateField_management("", "", "autoIncrement()", "PYTHON", "rec=0 \\ndef autoIncrement(): \\n global rec \\n pStart = 1  \\n pInterval = 1 \\n if (rec == 0):  \\n  rec = pStart  \\n else:  \\n  rec += pInterval  \\n return rec")


value = 1
for i in values:

        get length of list

        value for implementing =
