#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     26/06/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy

fc = r'C:\Users\UKPXR011\Desktop\Current Work\PCE Work\PCESample20200623\Scratch_Script.gdb\Plots_Lops'

with arcpy.da.UpdateCursor(fc,'SHAPE_Area') as updateRows:
    for updateRow in updateRows:
        if updateRow[0] <2:
            updateRows.deleteRow()
