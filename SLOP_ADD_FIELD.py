#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      UKPXR011
#
# Created:     29/03/2020
# Copyright:   (c) UKPXR011 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy

fc1 = r'Database Connections\HS2-Phase2B-Manchester-M2M3-Lot1-GSS.sde\HS2phase2B.GSS.STATUTORY_PROCESSES\HS2phase2B.GSS.Safeguarding_Land_Ownership_Parcels'



'''Repete this as many times as you need
arcpy.AddField_management(fc1, NAME, TYPE,"","",Length(if needed), "", "", "", "")

'''